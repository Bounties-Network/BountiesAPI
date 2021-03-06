# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-23 15:48
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_auto_20190212_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='emails',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'activity': False, 'both': {'RatingReceived': True}, 'fulfiller': {'ApplicationAcceptedApplicant': True, 'ApplicationRejectedApplicant': True, 'FulfillmentAcceptedFulfiller': True}, 'issuer': {'ApplicationReceived': True, 'BountyCommentReceived': True, 'BountyCompleted': True, 'BountyExpired': True, 'ContributionReceived': True, 'FulfillmentSubmittedIssuer': True, 'FulfillmentUpdatedIssuer': True, 'TransferRecipient': True}}),
        ),
    ]
