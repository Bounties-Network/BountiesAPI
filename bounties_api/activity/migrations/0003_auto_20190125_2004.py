# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-25 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('std_bounties', '0016_bounty_image_preview'),
        ('activity', '0002_auto_20190125_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bounty', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='std_bounties.Bounty')),
                ('comment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='std_bounties.Comment')),
                ('draft', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='std_bounties.DraftBounty')),
                ('fulfillment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='std_bounties.Fulfillment')),
            ],
        ),
        migrations.RemoveField(
            model_name='target',
            name='fulfillment',
        ),
        migrations.AddField(
            model_name='activity',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.Object'),
        ),
    ]
