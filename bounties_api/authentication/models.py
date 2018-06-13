import uuid
from django.apps import apps
from django.db import models
from django.contrib.postgres.fields import JSONField


class User(models.Model):
    profile_hash = models.CharField(max_length=128, blank=True)
    public_address = models.TextField(max_length=500, blank=True, unique=True)
    nonce = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    categories = models.ManyToManyField('std_bounties.Category', null=True)
    name = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=128, blank=True)
    organization = models.CharField(max_length=128, blank=True)
    languages = models.CharField(max_length=256, blank=True)
    profileFileName = models.CharField(max_length=256, blank=True)
    profileFileHash = models.CharField(max_length=256, blank=True)
    profileDirectoryHash = models.CharField(max_length=256, blank=True)
    profile_image = models.CharField(max_length=256, blank=True)
    website = models.CharField(max_length=128, blank=True)
    twitter = models.CharField(max_length=128, blank=True)
    github = models.CharField(max_length=128, blank=True)
    linkedin = models.CharField(max_length=128, blank=True)


class Settings(models.Model):
    user = models.ForeignKey(User, related_name='settings')
    emails = JSONField(null=True)
