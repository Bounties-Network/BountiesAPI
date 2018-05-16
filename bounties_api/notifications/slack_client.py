from django.conf import settings

from std_bounties.models import Fulfillment, Bounty, BountyState
from std_bounties.constants import ACTIVE_STAGE
from notifications.notification_templates import *
from notifications.constants import *
from slackclient import SlackClient as _SlackClient
from .base_clients import BaseClient


class SlackClient(BaseClient):
    def __init__(self,
                 client=_SlackClient(settings.SLACK_TOKEN),
                 channel=settings.NOTIFICATIONS_SLACK_CHANNEL):
        self.super(SlackClient, self).__init__()
        self.notify = wrapped_partial(notify_slack,
                                      client,
                                      channel)

    def fulfillment_submitted(self, bounty, fulfillment_id):
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)

        self.notify(event='Bounty Issued', msg=string_data_issuer)

    def bounty_activated(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        self.notify(event='Bounty Activated', msg=string_data)

    def fulfillment_accepted(self, bounty, fulfillment_id):
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data = FULFILLMENT_ACCEPTED_STR.format(bounty_title=bounty.title)
        self.notify(event='Bounty Accepted', msg=string_data)

    def bounty_expired(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify('Bounty Expired', msg=string_data)


    def issue_bounty(self, bounty, **kwargs):
        pass

    def update_fulfillment(self, bounty, **kwargs):
        pass

    def kill_bounty(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass

    def add_contribution(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass

    def extend_deadline(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass

    def change_bounty(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass

    def transfer_issuer(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass

    def increase_payout(self, bounty, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        pass
