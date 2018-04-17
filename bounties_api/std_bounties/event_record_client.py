class EventRecordClient:

    def __init__(self):
        pass


    def issue_bounty(self, bounty_id, inputs, event_timestamp):

        pass


    def activate_bounty(self, bounty, inputs):
        pass


    def fulfill_bounty(
            self,
            bounty,
            fulfillment_id,
            inputs,
            event_timestamp,
            transaction_issuer):
        pass


    def update_fulfillment(self, bounty, fulfillment_id, inputs):
        pass


    def accept_fulfillment(self, bounty, fulfillment_id, event_timestamp):
        pass


    def kill_bounty(self, bounty, event_timestamp):
        pass


    def add_contribution(self, bounty, inputs):
        pass


    def extend_deadline(self, bounty, inputs):
        pass


    def change_bounty(self, bounty, inputs):
        pass


    def transfer_issuer(self, bounty, inputs):
        pass


    def increase_payout(self, bounty, inputs):
        pass
