# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-26 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_squashed_0006_auto_20180504_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='bountiestimeline',
            name='is_week',
            field=models.BooleanField(default=False),
        ),
    ]
