# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-24 00:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0015_auto_20190212_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_name',
            field=models.IntegerField(choices=[(0, 'FulfillmentSubmitted'), (1, 'FulfillmentSubmittedIssuer'), (2, 'BountyActivated'), (3, 'FulfillmentAccepted'), (4, 'FulfillmentAcceptedFulfiller'), (14, 'BountyExpired'), (6, 'BountyIssued'), (7, 'BountyKilled'), (8, 'ContributionAdded'), (9, 'DeadlineExtended'), (10, 'BountyChanged'), (11, 'IssuerTransferred'), (12, 'TransferRecipient'), (13, 'PayoutIncreased'), (14, 'BountyExpired'), (15, 'BountyCommentReceived'), (16, 'BountyIssuedActivated'), (17, 'FulfillmentUpdated'), (18, 'FulfillmentUpdatedIssuer'), (19, 'RatingIssued'), (20, 'RatingReceived'), (21, 'ProfileUpdated'), (22, 'BountyComment'), (23, 'DraftCreated'), (24, 'DraftUpdated'), (25, 'ContributionReceived'), (26, 'BountyCompleted'), (27, 'ApplicationCreated'), (28, 'ApplicationReceived'), (29, 'ApplicationAcceptedApplicant'), (30, 'ApplicationAcceptedIssuer'), (31, 'ApplicationRejectedApplicant'), (32, 'ApplicationRejectedIssuer')]),
        ),
    ]
