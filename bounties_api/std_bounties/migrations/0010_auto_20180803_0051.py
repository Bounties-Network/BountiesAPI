# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-03 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('std_bounties', '0009_auto_20180802_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bounty',
            name='experienceLevel',
            field=models.IntegerField(choices=[(0, 'Beginner'), (1, 'Intermediate'), (2, 'Advanced')], null=True),
        ),
        migrations.AlterField(
            model_name='draftbounty',
            name='experienceLevel',
            field=models.IntegerField(choices=[(0, 'Beginner'), (1, 'Intermediate'), (2, 'Advanced')], null=True),
        ),
    ]
