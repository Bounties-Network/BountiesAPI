# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models
from std_bounties.constants import STAGE_CHOICES, DRAFT_STAGE


class Bounty(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    bounty_id = models.IntegerField()
    deadline = models.DateTimeField()
    data = models.CharField(max_length=128)
    issuer = models.CharField(max_length=128)
    arbiter = models.CharField(max_length=128, null=True)
    fulfillmentAmount = models.DecimalField(decimal_places=18, max_digits=64)
    paysTokens = models.BooleanField()
    bountystage = models.CharField(max_length=128, choices=STAGE_CHOICES, default=DRAFT_STAGE)
    old_balance = models.DecimalField(decimal_places=18, max_digits=64, null=True)
    balance = models.DecimalField(decimal_places=18, max_digits=64)
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    data_issuer = JSONField(null=True)
    funders = JSONField(null=True)
    categories = JSONField(null=True)
    bounty_created = models.DateTimeField(null=True)
    tokenSymbol = models.CharField(max_length=64, blank=True)
    tokenAddress = models.CharField(max_length=128, blank=True)
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceFileHash = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)
    webReferenceUrl = models.CharField(max_length=256, blank=True)
    platform = models.CharField(max_length=128, blank=True)
    schemaVersion = models.CharField(max_length=64, blank=True)
    schemaName = models.CharField(max_length=128, null=True)
    data_json = JSONField(null=True)


class Fulfillment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    fulfillment_id = models.IntegerField()
    data = models.CharField(max_length=128)
    bounty = models.ForeignKey(Bounty)
    accepted = models.BooleanField()
    fulfiller = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceFileHash = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)
    fulfiller = JSONField(null=True)
    platform = models.CharField(max_length=128, blank=True)
    schemaVersion = models.CharField(max_length=64, blank=True)
    schemaName = models.CharField(max_length=128, blank=True)
    data_json = JSONField(null=True)

