# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-19 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20181011_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='bountiestimeline',
            name='is_month',
            field=models.BooleanField(default=False),
        ),
    ]
