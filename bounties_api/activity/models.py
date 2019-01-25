from django.db import models

from activity.constants import ACTIVITY_TYPES
from user.models import User
from std_bounties.models import (
    Bounty,
    Comment,
    DraftBounty,
    Fulfillment
)


class Target(models.Model):
    bounty = models.OneToOneField(Bounty, null=True, blank=True, on_delete=models.CASCADE)
    draft = models.OneToOneField(DraftBounty, null=True, blank=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)


class Object(models.Model):
    bounty = models.OneToOneField(Bounty, null=True, blank=True, on_delete=models.CASCADE)
    draft = models.OneToOneField(DraftBounty, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.OneToOneField(Comment, null=True, blank=True, on_delete=models.CASCADE)
    fulfillment = models.OneToOneField(Fulfillment, null=True, blank=True, on_delete=models.CASCADE)


class Activity(models.Model):
    actor = models.ForeignKey('user.User', null=False)
    verb = models.CharField(max_length=3, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey('activity.Target', null=True)
    object = models.ForeignKey('activity.Object', null=True)
