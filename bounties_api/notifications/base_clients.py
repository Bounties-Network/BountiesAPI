class BaseClient:
    def __init__(self, client):
        if client:
            self._client = client

    def fulfillment_submitted(self, bounty_id, fulfillment_id):
        pass

    def bounty_activated(self, bounty_id):
        pass

    def fulfillment_accepted(self, bounty_id, fulfillment_id):
        pass

    def bounty_expired(self, bounty_id):
        pass

    def issue_bounty(self, bounty_id, **kwargs):
        pass

    def update_fulfillment(self, bounty, **kwargs):
        pass

    def kill_bounty(self, bounty, **kwargs):
        pass

    def add_contribution(self, bounty, **kwargs):
        pass

    def extend_deadline(self, bounty, **kwargs):
        pass

    def change_bounty(self, bounty, **kwargs):
        pass

    def transfer_issuer(self, bounty, **kwargs):
        pass

    def increase_payout(self, bounty, **kwargs):
        pass
