from slackclient import SlackClient as _SlackClient
from .base_clients import BaseClient


class SlackClient(BaseClient):
    def __init__(self):
        self.super(SlackClient, self).__init__(_SlackClient(settings.SLACK_TOKEN))

    def fulfillment_submitted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)

    def bounty_activated(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)



    def fulfillment_accepted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data = FULFILLMENT_ACCEPTED_STR.format(bounty_title=bounty.title)



    def bounty_expired(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)