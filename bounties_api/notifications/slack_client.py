from slackclient import SlackClient as _SlackClient

class SlackClient:
    def __init__(self):
        self._sc = _SlackClient(settings.SLACK_TOKEN)

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


    def issue_bounty(bounty_id, **kwargs):
        pass


    def bounty_activated(bounty_id):
        pass


    def fulfillment_submitted(bounty_id, **kwargs):
        pass



    def update_fulfillment(bounty, **kwargs):
        pass


    def fulfillment_accepted(bounty_id, **kwargs):
        pass

    def kill_bounty(bounty, **kwargs):
        pass


    def add_contribution(bounty, **kwargs):
        pass


    def extend_deadline(bounty, **kwargs):
        pass

    def change_bounty(bounty, **kwargs):
        pass


    def transfer_issuer(bounty, **kwargs):
        pass


    def increase_payout(bounty, **kwargs):
        pass
