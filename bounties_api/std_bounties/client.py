import datetime
from decimal import Decimal
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE
from std_bounties.client_helpers import map_bounty_data, map_token_data, map_fulfillment_data, get_token_pricing
from bounties.utils import getDateTimeFromTimestamp
from django.db import transaction
import logging


logger = logging.getLogger('django')

issue_bounty_input_keys = [
    'fulfillmentAmount',
    'arbiter',
    'paysTokens',
    'tokenContract',
    'value']


class BountyClient:

    def __init__(self):
        pass

    @transaction.atomic
    def issue_bounty(self, bounty_id, inputs, event_timestamp):
        bounty = Bounty.objects.filter(bounty_id=bounty_id).exists()
        if bounty:
            return

        data_hash = inputs.get('data', 'invalid')
        ipfs_data = map_bounty_data(data_hash, bounty_id)
        token_data = map_token_data(
            inputs.get('paysTokens'),
            inputs.get('tokenContract'),
            inputs.get('fulfillmentAmount'))

        plucked_inputs = {key: inputs.get(key)
                          for key in issue_bounty_input_keys}

        bounty_data = {
            'id': bounty_id,
            'bounty_id': bounty_id,
            'issuer': inputs.get(
                'issuer',
                '').lower(),
            'deadline': getDateTimeFromTimestamp(
                inputs.get(
                    'deadline',
                    None)),
            'bountyStage': DRAFT_STAGE,
            'bounty_created': datetime.datetime.fromtimestamp(
                    int(event_timestamp)),
        }

        bounty_serializer = BountySerializer(
            data={
                **bounty_data,
                **plucked_inputs,
                **ipfs_data,
                **token_data})
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()
        saved_bounty.save_and_clear_categories(
            ipfs_data.get('data_categories'))

    def activate_bounty(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.bountyStage = ACTIVE_STAGE
        bounty.save()

    def fulfill_bounty(
            self,
            bounty_id,
            fulfillment_id,
            inputs,
            event_timestamp,
            transaction_issuer):
        fulfillment = Fulfillment.objects.filter(
            fulfillment_id=fulfillment_id, bounty_id=bounty_id
        ).exists()
        if fulfillment:
            return

        data_hash = inputs.get('data')
        ipfs_data = map_fulfillment_data(data_hash, bounty_id, fulfillment_id)

        fulfillment_data = {
            'fulfillment_id': fulfillment_id,
            'fulfiller': transaction_issuer.lower(),
            'bounty': bounty_id,
            'accepted': False,
            'fulfillment_created': datetime.datetime.fromtimestamp(
                int(event_timestamp)),
        }

        fulfillment_serializer = FulfillmentSerializer(
            data={**fulfillment_data, **ipfs_data})
        fulfillment_serializer.is_valid(raise_exception=True)
        fulfillment_serializer.save()

    def update_fulfillment(self, bounty_id, fulfillment_id, inputs):
        data_hash = inputs.get('data')
        ipfs_data = map_fulfillment_data(data_hash, bounty_id, fulfillment_id)

        fulfillment = Fulfillment.objects.get(
            fulfillment_id=fulfillment_id, bounty_id=bounty_id)
        fulfillment_serializer = FulfillmentSerializer(
            fulfillment, data={**ipfs_data}, partial=True)
        fulfillment_serializer.save()

    def accept_fulfillment(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = bounty.balance - bounty.fulfillmentAmount
        if bounty.balance < bounty.fulfillmentAmount:
            bounty.bountyStage = COMPLETED_STAGE
        bounty.save()

        fulfillment = Fulfillment.objects.get(
            bounty_id=bounty_id, fulfillment_id=fulfillment_id)
        fulfillment.accepted = True
        fulfillment.save()

    def kill_bounty(self, bounty_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.old_balance = bounty.balance
        bounty.balance = 0
        bounty.bountyStage = DEAD_STAGE
        bounty.save()

    def add_contribution(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = Decimal(inputs.get('value'))
        if bounty.balance >= bounty.fulfillmentAmount and bounty.bountyStage == EXPIRED_STAGE:
            bounty.bountyStage = ACTIVE_STAGE
        bounty.save()

    def extend_deadline(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.deadline = getDateTimeFromTimestamp(
            inputs.get('newDeadline', None))
        bounty.save()

    @transaction.atomic
    def change_bounty(self, bounty_id, inputs):
        updated_data = {}
        data_hash = inputs.get('data', None)
        deadline = inputs.get('newDeadline', None)
        fulfillmentAmount = inputs.get('newFulfillmentAmount', None)
        arbiter = inputs.get('newArbiter', None)

        if data_hash:
            updated_data = map_bounty_data(data_hash, bounty_id)

        if deadline:
            updated_data['deadline'] = datetime.datetime.fromtimestamp(
                int(new_deadline))

        if fulfillmentAmount:
            updated_data['fulfillmentAmount'] = Decimal(fulfillmentAmount)

        if arbiter:
            updated_data['arbiter'] = arbiter

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty_serializer = BountySerializer(
            bounty, data=updated_data, partial=True)
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()

        if data_hash:
            saved_bounty.save_and_clear_categories(
                updated_data.get('data_categories'))

        if fulfillmentAmount:
            usd_price = get_token_pricing(
                saved_bounty.tokenSymbol,
                saved_bounty.tokenDecimals,
                fulfillmentAmount)[0]
            saved_bounty.usd_price = usd_price
            saved_bounty.save()

    def transfer_issuer(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.issuer = inputs.get('newIssuer')
        bounty.save()

    def increase_payout(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        value = inputs.get('value')
        fulfillment_amount = inputs.get('newFulfillmentAmount')
        if value:
            bounty.balance = bounty.balance + Decimal(value)
        usd_price = get_token_pricing(
            bounty.tokenSymbol,
            bounty.tokenDecimals,
            fulfillment_amount)[0]
        bounty.fulfillmentAmount = Decimal(fulfillment_amount)
        bounty.usd_price = usd_price
        bounty.save()
