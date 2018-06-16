import uuid
from django.apps import apps
from django.db import models
from django.contrib.postgres.fields import JSONField
from notifications.constants import default_email_options, rev_mapped_notifications


class Settings(models.Model):
    emails = JSONField(null=False, default=default_email_options)

    def readable_accepted_email_settings(self):
        merged_settings = {**self.emails['issuer'], **self.emails['both'], **self.emails['fulfiller']}
        return [setting for setting in merged_settings if merged_settings[setting]]

    def accepted_email_settings(self):
        merged_settings = {**self.emails['issuer'], **self.emails['both'], **self.emails['fulfiller']}
        return [rev_mapped_notifications[setting] for setting in merged_settings if merged_settings[setting]]


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
    github_username = models.CharField(max_length=128, blank=True)
    settings = models.ForeignKey(Settings, null=True)

    def save(self, *args, **kwargs):
        if not self.settings:
            self.settings = Settings.objects.create()
        super(User, self).save(*args, **kwargs)
