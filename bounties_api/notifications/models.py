from django.db import models


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    notification_created = models.DateTimeField(null=True)
    user = models.ForeignKey('authentication.User')
    viewed = models.BooleanField()
