# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-27 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20181020_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dismissed_signup_prompt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
