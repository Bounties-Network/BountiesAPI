from django.db import models
from django.contrib.postgres.fields import JSONField


class Notification(models.Model):
    user = models.ForeignKey('authentication.User', null=False)
    created = models.DateTimeField(auto_now_add=True)
    notification_id = models.IntegerField(null=False)
    notification_created = models.DateTimeField(null=False)
    email = models.BooleanField(default=False, null=False)
    dashboard = models.BooleanField(default=True, null=False)
    subscribed = models.BooleanField(default=True, null=False)


class NotificationDashboard(models.Model):
    notification = models.ForeignKey('Notification')
    viewed = models.BooleanField(default=False, null=False)
    string_data = models.CharField(max_length=512, blank=True)
    data = JSONField(null=True)
