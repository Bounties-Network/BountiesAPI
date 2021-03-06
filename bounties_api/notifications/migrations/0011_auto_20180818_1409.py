# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-18 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_auto_20180818_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_name',
            field=models.IntegerField(choices=[(0, 'FulfillmentSubmitted'), (1, 'FulfillmentSubmittedIssuer'), (2, 'BountyActivated'), (3, 'FulfillmentAccepted'), (4, 'FulfillmentAcceptedFulfiller'), (14, 'BountyExpired'), (6, 'BountyIssued'), (7, 'BountyKilled'), (8, 'ContributionAdded'), (9, 'DeadlineExtended'), (10, 'BountyChanged'), (11, 'IssuerTransferred'), (12, 'TransferRecipient'), (13, 'PayoutIncreased'), (14, 'BountyExpired'), (15, 'BountyCommentReceived'), (16, 'BountyIssuedActivated'), (17, 'FulfillmentUpdated'), (18, 'FulfillmentUpdatedIssuer'), (19, 'RatingIssued'), (20, 'RatingReceived'), (21, 'ProfileUpdated'), (22, 'BountyComment')]),
        ),
    ]
