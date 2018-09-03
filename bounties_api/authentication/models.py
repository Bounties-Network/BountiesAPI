import uuid
from django.apps import apps
from django.db import models

class User(models.Model):
    public_address = models.TextField(max_length=500, blank=True)
    nonce = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    categories = models.ManyToManyField('std_bounties.Category', null=True)
    name = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=128, blank=True)
    organization = models.CharField(max_length=128, blank=True)
    languages = models.CharField(max_length=256, blank=True)
    profileFileName = models.CharField(max_length=256, blank=True)
    profileFileHash = models.CharField(max_length=256, blank=True)
    profileDirectoryHash = models.CharField(max_length=256, blank=True)
    website = models.CharField(max_length=128, blank=True)
    twitter = models.CharField(max_length=128, blank=True)
    github = models.CharField(max_length=128, blank=True)
    linkedin = models.CharField(max_length=128, blank=True)
    email_notifications = models.BooleanField(default=True)
