# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models
from std_bounties.constants import STAGE_CHOICES, DRAFT_STAGE
from django.core.exceptions import ObjectDoesNotExist


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    normalized_name = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.lower().strip()
        super(Category, self).save(*args, **kwargs)


class Token(models.Model):
    normalized_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    price_usd = models.FloatField(default=0, null=True)


class Bounty(models.Model):
    id = models.IntegerField(primary_key=True)
    bounty_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, null=True)
    deadline = models.DateTimeField()
    data = models.CharField(max_length=128)
    issuer = models.CharField(max_length=128)
    arbiter = models.CharField(max_length=128, null=True)
    fulfillmentAmount = models.DecimalField(decimal_places=0, max_digits=64)
    paysTokens = models.BooleanField()
    bountyStage = models.IntegerField(
        choices=STAGE_CHOICES, default=DRAFT_STAGE)
    old_balance = models.DecimalField(
        decimal_places=0, max_digits=64, null=True)
    balance = models.DecimalField(
        decimal_places=0,
        max_digits=70,
        null=True,
        default=0)
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    bounty_created = models.DateTimeField(null=True)
    token = models.ForeignKey(Token, null=True)
    tokenSymbol = models.CharField(max_length=128, default='ETH')
    tokenDecimals = models.IntegerField(default=18)
    tokenContract = models.CharField(
        max_length=128,
        default='0x0000000000000000000000000000000000000000')
    usd_price = models.FloatField(default=0)
    issuer_name = models.CharField(max_length=128, blank=True)
    issuer_email = models.CharField(max_length=128, blank=True)
    issuer_githubUsername = models.CharField(max_length=128, blank=True)
    issuer_address = models.CharField(max_length=128, blank=True)
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceFileHash = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)
    webReferenceUrl = models.CharField(max_length=256, blank=True)
    platform = models.CharField(max_length=128, blank=True)
    schemaVersion = models.CharField(max_length=64, blank=True)
    schemaName = models.CharField(max_length=128, null=True)
    data_categories = JSONField(null=True)
    data_issuer = JSONField(null=True)
    data_json = JSONField(null=True)

    def save_and_clear_categories(self, categories):
        # this is really messy, but this is bc of psql django bugs
        self.categories.clear()
        if isinstance(categories, list):
            for category in categories:
                if isinstance(category, str):
                    try:
                        matching_category = Category.objects.get(
                            name=category.strip())
                        self.categories.add(matching_category)
                    except ObjectDoesNotExist:
                        self.categories.create(name=category.strip())


class Fulfillment(models.Model):
    fulfillment_id = models.IntegerField()
    bounty = models.ForeignKey(Bounty, related_name='fulfillments')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    fulfillment_created = models.DateTimeField(null=True)
    data = models.CharField(max_length=128)
    accepted = models.BooleanField()
    fulfiller = models.CharField(max_length=128)
    fulfiller_name = models.CharField(max_length=128, blank=True)
    fulfiller_email = models.CharField(max_length=128, blank=True)
    fulfiller_githubUsername = models.CharField(max_length=128, blank=True)
    fulfiller_address = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceFileHash = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)
    platform = models.CharField(max_length=128, blank=True)
    schemaVersion = models.CharField(max_length=64, blank=True)
    schemaName = models.CharField(max_length=128, blank=True)
    data_fulfiller = JSONField(null=True)
    data_json = JSONField(null=True)


class RankedCategory(models.Model):
    name = models.CharField(max_length=128)
    normalized_name = models.CharField(max_length=128)
    total_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'category_ranks'
