from django.db import models


class Notification(models.Model):
    user = models.ForeignKey('authentication.User', null=False)
    created = models.DateTimeField(auto_now_add=True)
    notification_id = models.IntegerField(null=False)
    notification_created = models.DateTimeField(null=False)
    email = models.BooleanField(default=False, null=False)
    dashboard = models.BooleanField(default=True, null=False)
    subscribed = models.BooleanField(default=True, null=False)
    viewed = models.BooleanField(default=False, null=False)
