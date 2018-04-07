from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    class Meta:
        unique_together = (('transaction_hash', 'event_name'),)

    event_name = models.CharField(max_length=128)
    transaction_hash = models.CharField(max_length=128)
    bounty_id = models.IntegerField()
    fulfillment_id = models.IntegerField()
    transaction_from = models.CharField(max_length=128)
    event_timestamp = models.IntegerField()
    contract_method_inputs = JSONField(null=True)
