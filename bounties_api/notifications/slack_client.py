from django.conf import settings

from std_bounties.models import Fulfillment, Bounty, BountyState
from std_bounties.constants import ACTIVE_STAGE
from notifications.notification_templates import *
from notifications.constants import *
from slackclient import SlackClient as _SlackClient
from .base_clients import BaseClient


class Events(Enum):
    FULFILLMENT_SUBMITTED='Bounty Issued'
    BOUNTY_ACTIVATED='Bounty Activated'
    FULFILLMENT_SUBMITTED='Bounty Fulfillment Submitted'
    bounty_activated='Bounty Activated'
    FULFILLMENT_ACCEPTED='Bounty Fulfillment Accepted'
    BOUNTY_EXPIRED='Bounty Expired'
    ISSUE_BOUNTY='Bounty Issued'
    UPDATE_FULFILLMENT='Bounty Fulfillment Updated'
    KILL_BOUNTY = 'Bounty Killed'
    ADD_CONTRIBUTION='Contribution Added'
    EXTEND_DEADLINE="Deadline Extended"
    CHANGE_BOUNTY='Bounty Changed'
    TRANSFER_ISSUER = 'Issuer Transfered'
    INCREASE_PAYOUT = 'Payout Increased'



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

        self.notify(event=Events.FULFILLMENT_SUBMITTED.value, msg=string_data_issuer)

    def bounty_activated(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        self.notify(event=Events.BOUNTY_ACTIVATED.value, msg=string_data)

    def fulfillment_accepted(self, bounty, fulfillment_id):
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data = FULFILLMENT_ACCEPTED_STR.format(bounty_title=bounty.title)
        self.notify(event=Events.FULFILLMENT_ACCEPTED.value, msg=string_data)

    def bounty_expired(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(event=Events.BOUNTY_EXPIRED.value, msg=string_data)

    def issue_bounty(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(event=Events.ISSUE_BOUNTY.value, msg=string_data)

    def update_fulfillment(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.UPDATE_FULFILLMENT.value, msg=string_data)

    def kill_bounty(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.KILL_BOUNTY, msg=string_data)

    def add_contribution(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.ADD_CONTRIBUTION.value, msg=string_data)

    def extend_deadline(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.EXTEND_DEADLINE.value, msg=string_data)

    def change_bounty(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.CHANGE_BOUNTY.value, msg=string_data)

    def transfer_issuer(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.TRANSFER_ISSUER.value, msg=string_data)

    def increase_payout(self, bounty, **kwargs):
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        self.notify(Events.INCREASE_PAYOUT.value, msg=string_data)
