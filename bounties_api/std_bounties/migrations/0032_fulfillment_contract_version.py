# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-14 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('std_bounties', '0031_contribution_contribution_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulfillment',
            name='contract_version',
            field=models.IntegerField(choices=[(1, 'v1'), (2, 'v2')], default=1),
        ),
    ]
