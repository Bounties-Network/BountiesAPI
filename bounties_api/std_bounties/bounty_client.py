import json
import datetime
from decimal import Decimal
from std_bounties.models import Contribution, Fulfillment, DraftBounty
from std_bounties.serializers import BountySerializer, ContributionSerializer, FulfillmentSerializer
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE, STANDARD_BOUNTIES_V1
from std_bounties.client_helpers import map_bounty_data, map_token_data, map_fulfillment_data, get_token_pricing, get_historic_pricing
from user.models import User
from bounties.utils import getDateTimeFromTimestamp
from django.db import transaction
import logging


logger = logging.getLogger('django')

issue_bounty_input_keys = [
    'fulfillmentAmount',
    'arbiter',
    'paysTokens',
    'token_contract',
    'value'
]


class BountyClient:

    def __init__(self):
        pass

    @transaction.atomic
    def issue_bounty(self, bounty_id, contract_version, **kwargs):
        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))

        ipfs_data = map_bounty_data(kwargs.get('data', ''), bounty_id)
        token_data = map_token_data(kwargs.get('token_version'), kwargs.get('token'), 0)

        # TODO what happens if issuers or approvers is actually blank?
        contract_state = {'issuers': {}, 'approvers': {}}
        issuers = []
        for index, issuer in enumerate(kwargs.get('issuers', [])):
            user = User.objects.get_or_create(public_address=issuer.lower())[0]
            issuers.append(user.pk)
            contract_state['issuers'].update({issuer.lower(): index})

        approvers = []
        for index, approver in enumerate(kwargs.get('approvers', [])):
            user = User.objects.get_or_create(public_address=approver.lower())[0]
            approvers.append(user.pk)
            contract_state['approvers'].update({approver.lower(): index})

        bounty_data = {
            'bounty_id': bounty_id,
            'contract_version': contract_version,

            # legacy for stb 1.0
            'user': issuers[0],
            'issuer': kwargs.get('issuers')[0].lower(),
            ###

            'issuers': issuers,
            'approvers': approvers,
            'contract_state': json.dumps(contract_state),
            'deadline': getDateTimeFromTimestamp(kwargs.get('deadline', None)),
            'bounty_stage': DEAD_STAGE,
            'bounty_created': event_date,
        }

        if contract_version == STANDARD_BOUNTIES_V1:
            bounty_data.update({'fulfillment_amount': kwargs.get('fulfillment_amount')})
        else:
            bounty_data.update({'fulfillment_amount': ipfs_data.get('fulfillment_amount')})

        bounty_serializer = BountySerializer(data={
            **bounty_data,
            **ipfs_data,
            **token_data
        })

        bounty_serializer.is_valid(raise_exception=True)

        saved_bounty = bounty_serializer.save()
        saved_bounty.save_and_clear_categories(ipfs_data.get('data_categories'))
        saved_bounty.bounty_stage = ACTIVE_STAGE
        saved_bounty.record_bounty_state(event_date)

        uid = saved_bounty.uid

        if uid:
            DraftBounty.objects.filter(uid=uid).update(on_chain=True)

        print('bounty info: ', saved_bounty.id, saved_bounty.contract_version, saved_bounty.token_contract, saved_bounty.revisions)
        return saved_bounty

    def activate_bounty(self, bounty, **kwargs):
        if bounty.bounty_stage == ACTIVE_STAGE:
            print('Activating a bounty that is already active')  # maybe this should be an error

        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))
        bounty.bounty_stage = ACTIVE_STAGE
        bounty.record_bounty_state(event_date)
        bounty.save()

        return bounty

    def fulfill_bounty(self, bounty, **kwargs):
        fulfillment_id = kwargs.get('fulfillment_id')

        data_hash = kwargs.get('data')
        ipfs_data = map_fulfillment_data(data_hash, bounty.bounty_id, fulfillment_id)
        
        fulfillment_data = {
            'contract_version': bounty.contract_version,
            'fulfillment_id': fulfillment_id,
            'fulfiller_address': kwargs.get('fulfillers')[0].lower(),
            'fulfiller': kwargs.get('fulfillers')[0].lower(),
            'bounty': bounty.pk,
            'accepted': False,
            'fulfillment_created': datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp'))),
        }

        fulfillment_serializer = FulfillmentSerializer(data={
            **fulfillment_data,
            **ipfs_data
        })

        fulfillment_serializer.is_valid(raise_exception=True)

        return fulfillment_serializer.save()

    def update_fulfillment(self, bounty, fulfillment_id, inputs, **kwargs):
        fulfillment = Fulfillment.objects.get(
            fulfillment_id=fulfillment_id, bounty_id=bounty.bounty_id)

        data_hash = inputs.get('data')
        ipfs_data = map_fulfillment_data(
            data_hash, bounty.bounty_id, fulfillment_id)

        fulfillment_serializer = FulfillmentSerializer(
            fulfillment, data={**ipfs_data}, partial=True)
        instance = fulfillment_serializer.save()

        return instance

    @transaction.atomic
    def accept_fulfillment(self, bounty, **kwargs):
        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))
        bounty.balance = bounty.balance - bounty.fulfillment_amount

        usd_price, token_price = get_historic_pricing(
            bounty.token_symbol,
            bounty.token_decimals,
            bounty.fulfillment_amount,
            kwargs.get('event_timestamp')
        )

        if bounty.balance < bounty.fulfillment_amount:
            bounty.bounty_stage = COMPLETED_STAGE
            bounty.usd_price = usd_price
            bounty.token_lock_price = token_price
            bounty.record_bounty_state(event_date)

        bounty.save()

        fulfillment = Fulfillment.objects.get(bounty=bounty.pk, fulfillment_id=kwargs.get('fulfillment_id'))
        fulfillment.accepted = True
        fulfillment.usd_price = usd_price
        fulfillment.accepted_date = getDateTimeFromTimestamp(kwargs.get('event_timestamp'))
        fulfillment.save()

        return fulfillment

    def kill_bounty(self, bounty, **kwargs):
        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))

        bounty.old_balance = bounty.balance
        bounty.balance = 0

        usd_price, token_price = get_historic_pricing(
            bounty.token_symbol,
            bounty.token_decimals,
            bounty.fulfillment_amount,
            kwargs.get('event_timestamp')
        )

        has_accepted_fulfillments = bounty.fulfillments.filter(accepted=True).exists()

        if has_accepted_fulfillments:
            bounty.bounty_stage = COMPLETED_STAGE
        else:
            bounty.bounty_stage = DEAD_STAGE

        bounty.usd_price = usd_price
        bounty.token_lock_price = token_price
        bounty.record_bounty_state(event_date)
        bounty.save()

        return bounty

    def add_contribution(self, bounty, **kwargs):
        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))
        bounty.balance = Decimal(bounty.balance) + Decimal(kwargs.get('value', kwargs.get('amount')))

        # not sure about this ... what if the bounty expired because the deadline passed?
        if bounty.balance >= bounty.fulfillment_amount and bounty.bounty_stage == EXPIRED_STAGE:
            bounty.bounty_stage = ACTIVE_STAGE
            bounty.record_bounty_state(event_date)

        if bounty.balance >= bounty.fulfillment_amount and (bounty.bounty_stage == COMPLETED_STAGE or bounty.bounty_stage == DEAD_STAGE):
            bounty.bounty_stage = ACTIVE_STAGE
            bounty.record_bounty_state(event_date)
            bounty.usd_price = get_token_pricing(
                bounty.token_symbol,
                bounty.token_decimals,
                bounty.fulfillment_amount
            )[0]

        bounty.save()

        contribution_serializer = ContributionSerializer(data={
            'contributor': User.objects.get_or_create(public_address=kwargs.get('contributor').lower())[0].pk,
            'bounty': bounty.pk,
            'contribution_id': kwargs.get('contribution_id'),
            'amount': kwargs.get('amount'),
            # 'raw_event_data': json.dumps(kwargs),
        })

        contribution_serializer.is_valid(raise_exception=True)
        contribution = contribution_serializer.save()

        return contribution

    def refund_contribution(self, bounty, **kwargs):
        contribution = Contribution.objects.get(bounty=bounty.pk, contribution_id=kwargs.get('contribution_id'))
        contribution.refunded = True

        bounty.balance = Decimal(bounty.balance) - Decimal(contribution.amount)

        if bounty.balance < bounty.fulfillment_amount and bounty.bounty_stage == ACTIVE_STAGE:
            # TODO: set bounty to completed or expired
            pass

        bounty.save()

        return contribution.save()

    def change_deadline(self, bounty, **kwargs):
        event_date = datetime.datetime.fromtimestamp(int(kwargs.get('event_timestamp')))
        bounty.deadline = getDateTimeFromTimestamp(kwargs.get('deadline'))

        if bounty.deadline > datetime.datetime.now() and bounty.bounty_stage == EXPIRED_STAGE:
            bounty.bounty_stage = ACTIVE_STAGE
            bounty.record_bounty_state(event_date)
        elif bounty.deadline < datetime.datetime.now() and bounty.bounty_stage == ACTIVE_STAGE:
            bounty.bounty_stage = EXPIRED_STAGE
            bounty.record_bounty_state(event_date)

        bounty.save()

        return bounty

    def change_data(self, bounty, **kwargs):
        updated_data = {}

        updated_data = map_bounty_data(kwargs.get('data'), bounty.bounty_id)

        bounty_serializer = BountySerializer(bounty, data=updated_data, partial=True)
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()

        saved_bounty.save_and_clear_categories(updated_data.get('data_categories'))

        return saved_bounty

    def update_bounty_issuers(self, bounty, **kwargs):
        bounty.issuers.clear()

        issuers = kwargs.get('issuers')
        issuers_state = {}
        for (index, issuer) in enumerate(issuers):
            bounty.issuers.add(User.objects.get_or_create(public_address=issuer.lower())[0].pk)
            issuers_state.update({issuer.lower(): index})

        contract_state = json.loads(bounty.contract_state)
        contract_state.update({'issuers': issuers_state})
        bounty.contract_state = json.dumps(contract_state)

        bounty.save()

        return bounty

    def update_bounty_approvers(self, bounty, **kwargs):
        bounty.approvers.clear()

        approvers = kwargs.get('approvers')
        approvers_state = {}
        for (index, approver) in enumerate(approvers):
            bounty.approvers.add(User.objects.get_or_create(public_address=approver.lower())[0].pk)
            approvers_state.update({approver.lower(): index})

        contract_state = json.loads(bounty.contract_state)
        contract_state.update({'approvers': approvers_state})
        bounty.contract_state = json.dumps(contract_state)

        bounty.save()

        return bounty

    @transaction.atomic
    def change_bounty(self, bounty, **kwargs):
        bounty = self.change_data(bounty, **kwargs)
        bounty = self.change_deadline(bounty, **kwargs)
        bounty = self.update_bounty_issuers(bounty, **kwargs)
        bounty = self.update_bounty_approvers(bounty, **kwargs)

        return bounty

    def increase_payout(self, bounty, **kwargs):
        fulfillment_amount = kwargs.get('fulfillment_amount')

        usd_price = get_token_pricing(
            bounty.token_symbol,
            bounty.token_decimals,
            fulfillment_amount
        )[0]

        bounty.fulfillmentAmount = Decimal(fulfillment_amount)
        bounty.usd_price = usd_price
        bounty.save()

        return bounty
