from django.db import models
from django.contrib.postgres.fields import JSONField
from notifications.constants import NOTIFICATION_IDS


class Notification(models.Model):
    user = models.ForeignKey('user.User', null=False)
    uid = models.CharField(null=False, blank=False, max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notification_name = models.IntegerField(choices=NOTIFICATION_IDS, null=False)
    notification_created = models.DateTimeField(null=False)
    email_sent = models.BooleanField(default=False, null=False)
    dashboard = models.BooleanField(default=True, null=False)


class DashboardNotification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey(Notification, null=False)
    is_activity = models.BooleanField(default=False, null=False)
    viewed = models.BooleanField(default=False, null=False)
    string_data = models.CharField(max_length=512, blank=True)
    data = JSONField(null=True)


class Transaction(models.Model):
    user = models.ForeignKey('user.User', null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tx_hash = models.CharField(max_length=256, null=False, blank=False, unique=True)
    failed = models.BooleanField(default=False, null=False)
    completed = models.BooleanField(default=False, null=False)
    viewed = models.BooleanField(default=False, null=False)
    data = JSONField(null=True)
