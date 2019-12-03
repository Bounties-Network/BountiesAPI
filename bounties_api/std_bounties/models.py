# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import json
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
from std_bounties.constants import STAGE_CHOICES, DIFFICULTY_CHOICES, \
    DRAFT_STAGE, EXPIRED_STAGE, ACTIVE_STAGE, TOKEN_CHOICES
from django.core.exceptions import ObjectDoesNotExist
from bounties.utils import calculate_token_value
from django.contrib.postgres.fields import JSONField, ArrayField


class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    reviewer = models.ForeignKey(User, related_name='reviews')
    reviewee = models.ForeignKey(User, related_name='reviewees')
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)])
    review = models.TextField(blank=True)
    platform = models.CharField(max_length=128, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    normalized_name = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.lower().strip()
        super(Category, self).save(*args, **kwargs)


class Community(models.Model):
    community_id = models.CharField(max_length=128, blank=True)
    community_name = models.CharField(max_length=128, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    small_profile_image_url = models.CharField(max_length=256, blank=True)
    large_profile_image_url = models.CharField(max_length=256, blank=True)
    public = models.BooleanField(default=True)
    admin_user = models.ForeignKey(User)
    password = models.CharField(max_length=256, blank=True)
    network = models.CharField(max_length=256, default='mainNet')


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User')
    text = models.TextField()
    community = models.ForeignKey(Community, null=True)


class Token(models.Model):
    normalized_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    price_usd = models.FloatField(default=0, null=True)


class BountyState(models.Model):
    bounty = models.ForeignKey('Bounty')
    bounty_stage = models.IntegerField(null=False)
    change_date = models.DateTimeField(null=False)

    def save(self, *args, **kwargs):
        # Until we have a better event system, this logic is needed for when we resync to the
        # blockchain. Since expired is mutable, we need to make sure it was applied after the
        # other events - see track_bounty_expirations
        queryset = BountyState.objects.filter(bounty=self.bounty)
        if queryset.exists():
            last_record = queryset.latest()
            last_stage = last_record.bounty_stage
            if last_stage == EXPIRED_STAGE and self.change_date < last_record.change_date:
                last_record.delete()
            if last_stage == ACTIVE_STAGE and self.bounty.deadline < self.change_date:
                BountyState.objects.create(
                    bounty=self.bounty,
                    bounty_stage=EXPIRED_STAGE,
                    change_date=self.bounty.deadline
                )
        super(BountyState, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = 'change_date'


class BountyAbstract(models.Model):
    # legacy fields
    user = models.ForeignKey('user.User', null=True)

    # bounty data
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    revisions = models.IntegerField(null=True)
    categories = models.ManyToManyField(Category)
    deadline = models.DateTimeField()

    # user data
    issuer_name = models.CharField(max_length=128, blank=True)
    issuer_email = models.CharField(max_length=128, blank=True)
    issuer_githubUsername = models.CharField(max_length=128, blank=True)
    issuer_address = models.CharField(max_length=128, blank=True)

    # attached data
    attached_filename = models.CharField(max_length=256, blank=True, null=True)
    attached_data_hash = models.CharField(
        max_length=256, blank=True, null=True)
    attached_url = models.CharField(max_length=256, blank=True, null=True)

    # token info
    token = models.ForeignKey(Token, null=True)
    token_symbol = models.CharField(max_length=128, default='ETH')
    token_decimals = models.IntegerField(default=18)
    token_version = models.IntegerField(choices=TOKEN_CHOICES, null=True)
    token_contract = models.CharField(
        max_length=128, default='0x0000000000000000000000000000000000000000')

    # payout info
    usd_price = models.FloatField(default=0)
    fulfillment_amount = models.DecimalField(
        decimal_places=0, max_digits=64, default=0)
    calculated_fulfillment_amount = models.DecimalField(
        decimal_places=30,
        max_digits=70,
        null=True,
        default=0
    )

    # flags
    private_fulfillments = models.BooleanField(default=True)
    fulfillers_need_approval = models.BooleanField(default=False)

    # metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    schema_version = models.CharField(max_length=64, blank=True)
    schema_name = models.CharField(max_length=128, null=True)
    platform = models.CharField(
        max_length=128, blank=True, default="bounties-network")
    community = models.ForeignKey(Community, null=True)
    network = models.CharField(max_length=256, default='mainNet')

    class Meta:
        abstract = True


class Bounty(BountyAbstract):
    # legacy fields
    issuer = models.CharField(max_length=128)

    # role-based access controls
    issuers = models.ManyToManyField(
        User, related_name="%(app_label)s_%(class)s_related", )
    approvers = models.ManyToManyField(
        User, related_name="%(app_label)s_%(class)s_relateda", )

    # id fields
    bounty_id = models.IntegerField()
    uid = models.CharField(max_length=128, blank=True, null=True)
    contract_version = models.CharField(max_length=64, blank=True)

    # other fields
    contract_state = JSONField(null=True)
    bounty_created = models.DateTimeField(null=True)
    bounty_stage = models.IntegerField(
        choices=STAGE_CHOICES, default=DRAFT_STAGE)
    comments = models.ManyToManyField(Comment, related_name='bounty_comments')
    experience_level = models.IntegerField(
        choices=DIFFICULTY_CHOICES, null=True)

    data = models.CharField(max_length=128)
    old_balance = models.DecimalField(
        decimal_places=0, max_digits=64, null=True)

    token_lock_price = models.FloatField(null=True, blank=True)

    balance = models.DecimalField(
        decimal_places=0,
        max_digits=70,
        null=True,
        default=0)

    calculated_balance = models.DecimalField(
        decimal_places=30,
        max_digits=70,
        null=True,
        default=0)

    image_preview = models.CharField(max_length=256, blank=True)

    data_categories = JSONField(null=True)
    data_issuer = JSONField(null=True)
    data_json = JSONField(null=True)

    raw_ipfs_data = JSONField(null=True)
    raw_event_data = JSONField(null=True)
    view_count = models.IntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        fulfillment_amount = self.fulfillment_amount
        balance = self.balance
        decimals = self.token_decimals
        self.calculated_balance = calculate_token_value(balance, decimals)
        self.calculated_fulfillment_amount = calculate_token_value(
            fulfillment_amount, decimals)
        issuers = json.loads(self.contract_state or '{}').get('issuers', None)

        if issuers:
            issuer = next(
                (address for address, index in issuers.items() if index == 0), None)
            user, created = User.objects.get_or_create(
                public_address=issuer.lower(),
                defaults={
                    'name': self.issuer_name,
                    'email': self.issuer_email,
                    'github': self.issuer_githubUsername,
                }
            )
            self.user = user
            self.issuer = issuer

        super(Bounty, self).save(*args, **kwargs)

    def record_bounty_state(self, event_date):
        """Makes sure no duplicates are created"""
        # Need to make this a post_event signal. The only problem is we need a better event system
        # since this call requires an event_date
        return BountyState.objects.get_or_create(
            bounty=self, bounty_stage=self.bounty_stage, change_date=event_date)

    def save_and_clear_categories(self, categories):
        # this is really messy, but this is bc of psql django bugs
        self.categories.clear()
        if isinstance(categories, list):
            for category in categories:
                if isinstance(category, str):
                    try:
                        if category != '':
                            matching_category = Category.objects.get(
                                name=category.strip())
                            self.categories.add(matching_category)
                    except ObjectDoesNotExist:
                        self.categories.create(name=category.strip())

    class Meta:
        indexes = [
            models.Index(fields=['bounty_id', 'contract_version']),
        ]


class DraftBounty(BountyAbstract):
    uid = models.UUIDField(default=uuid.uuid4)
    data = models.CharField(max_length=128, null=True, blank=True)
    issuer = models.CharField(max_length=128, null=True, blank=True)
    on_chain = models.BooleanField(default=False)
    experience_level = models.IntegerField(
        choices=DIFFICULTY_CHOICES, null=True)
    platform = models.CharField(max_length=128, blank=True)
    data_categories = None
    data_issuer = None
    data_json = None
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        fulfillment_amount = self.fulfillment_amount
        decimals = self.token_decimals
        self.calculated_fulfillment_amount = calculate_token_value(
            fulfillment_amount, decimals)
        super(DraftBounty, self).save(*args, **kwargs)


class Fulfillment(models.Model):
    fulfillment_id = models.IntegerField()
    user = models.ForeignKey('user.User', null=True)
    bounty = models.ForeignKey(Bounty, related_name='fulfillments')
    contract_version = models.CharField(max_length=64, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    fulfillment_created = models.DateTimeField(null=True)
    fulfiller_review = models.ForeignKey(
        Review, related_name='fulfillment_review', null=True)
    issuer_review = models.ForeignKey(
        Review, related_name='issuer_review', null=True)
    data = models.CharField(max_length=128)
    accepted = models.BooleanField()
    accepted_date = models.DateTimeField(null=True)
    usd_price = models.FloatField(null=True)
    fulfiller = models.CharField(max_length=128)
    fulfiller_name = models.CharField(max_length=128, blank=True)
    fulfiller_email = models.CharField(max_length=128, blank=True)
    fulfiller_githubUsername = models.CharField(max_length=128, blank=True)
    fulfiller_address = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=256, blank=True)
    sourceFileName = models.CharField(max_length=256, blank=True)
    sourceFileHash = models.CharField(max_length=256, blank=True)
    sourceDirectoryHash = models.CharField(max_length=256, blank=True)
    platform = models.CharField(max_length=128, blank=True)
    schemaVersion = models.CharField(max_length=64, blank=True)
    schemaName = models.CharField(max_length=128, blank=True)
    data_fulfiller = JSONField(null=True)
    data_json = JSONField(null=True)
    fulfillers = ArrayField(models.CharField(max_length=128), null=True)
    comments = models.ManyToManyField(Comment, related_name='fulfillment_comments')
    community = models.ForeignKey(Community, null=True)
    network = models.CharField(max_length=256, default='mainNet')

    def save(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            public_address=self.fulfiller,
            defaults={
                'name': self.fulfiller_name,
                'email': self.fulfiller_email,
                'github': self.fulfiller_githubUsername,
            }
        )
        if not created and not user.profile_touched_manually:
            user.name = self.fulfiller_name if self.fulfiller_name else user.name
            user.email = self.fulfiller_email if self.fulfiller_email else user.email
            user.save()
        self.user = user
        super(Fulfillment, self).save(*args, **kwargs)


class RankedCategory(models.Model):
    name = models.CharField(max_length=128)
    normalized_name = models.CharField(max_length=128)
    total_count = models.IntegerField()
    platform = models.CharField(max_length=128, blank=False, default='main')

    class Meta:
        managed = False
        db_table = 'category_ranks'


class Event(models.Model):
    event = models.CharField(max_length=128)
    bounty = models.ForeignKey(Bounty, null=True)
    # corresponds to fulfillment_id not the fullfillment pk or id
    fulfillment_id = models.IntegerField(null=True)
    transaction_hash = models.CharField(max_length=128)
    transaction_from = models.CharField(max_length=128)
    contract_inputs = JSONField(null=True)
    contract_event_data = JSONField(null=True)
    event_date = models.DateTimeField()
    network = models.CharField(max_length=256, default='mainNet')


class Contribution(models.Model):
    contributor = models.ForeignKey(User)
    bounty = models.ForeignKey(Bounty)

    refunded = models.BooleanField(default=False)
    contribution_id = models.IntegerField()

    amount = models.DecimalField(decimal_places=0, max_digits=64)
    calculated_amount = models.DecimalField(
        decimal_places=30, max_digits=70, null=True, default=0)
    usd_amount = models.FloatField(default=0)

    platform = models.CharField(
        max_length=128, blank=True, default='bounties-network')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    raw_event_data = JSONField(null=True)

    def save(self, *args, **kwargs):
        amount = self.amount
        decimals = self.bounty.token_decimals
        self.calculated_amount = calculate_token_value(amount, decimals)

        super(Contribution, self).save(*args, **kwargs)


class FulfillerApplication(models.Model):
    ACCEPTED = 'A'
    REJECTED = 'R'
    PENDING = 'P'

    APPLICATION_STATES = (
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (PENDING, 'pending'),
    )

    bounty = models.ForeignKey(Bounty, blank=False, null=False)
    applicant = models.ForeignKey('user.User')
    message = models.TextField()
    state = models.CharField(
        max_length=1, choices=APPLICATION_STATES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    issuer_reply = models.TextField(default='')


class View(models.Model):
    bounty = models.ForeignKey(Bounty)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', null=True)


class Contract(models.Model):
    contract_type = models.CharField(max_length=64, blank=True)
    contract_version = models.CharField(max_length=64, blank=True)
    contract_address = models.CharField(max_length=128, blank=True)
    abi = JSONField(null=True)
    network = models.CharField(max_length=256, default='mainNet')


class Activity(models.Model):
    event_type = models.CharField(max_length=128)
    bounty = models.ForeignKey(Bounty, null=True)
    fulfillment = models.ForeignKey(Fulfillment, null=True)
    comment = models.ForeignKey(Comment, null=True)
    user = models.ForeignKey(User)
    community = models.ForeignKey(Community, null=True)
    transaction_hash = models.CharField(max_length=256, blank=True)
    date = models.DateTimeField(null=True)
