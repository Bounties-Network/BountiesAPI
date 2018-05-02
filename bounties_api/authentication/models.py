import uuid
from django.db import models

class User(models.Model):
    public_address = models.TextField(max_length=500, blank=True)
    nonce = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    name = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=128, blank=True)
