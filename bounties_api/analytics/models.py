from django.db import models


class BountiesTimeline(models.Model):
    date = models.DateField()
    bounties_issued = models.PositiveIntegerField()
    fulfillments_submitted = models.PositiveIntegerField()
    fulfillments_accepted = models.PositiveIntegerField()
    fulfillments_pending_acceptance = models.PositiveIntegerField()
    fulfillment_acceptance_rate = models.FloatField()
    bounty_fulfilled_rate = models.FloatField()
    avg_fulfiller_acceptance_rate = models.FloatField()
    avg_fulfillment_amount = models.FloatField()
    total_fulfillment_amount = models.DecimalField(decimal_places=0, max_digits=64)
    bounty_draft = models.PositiveIntegerField()
    bounty_active = models.PositiveIntegerField()
    bounty_completed = models.PositiveIntegerField()
    bounty_expired = models.PositiveIntegerField()
    bounty_dead = models.PositiveIntegerField()
