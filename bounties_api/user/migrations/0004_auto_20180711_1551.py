# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-11 15:14
from __future__ import unicode_literals

import csv
from django.db import migrations, models


def add_languages(apps, schema_editor):
    Language = apps.get_model('user', 'Language')

    with open('./std_bounties/fixtures/languages.csv') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [r for r in reader]

        for line in data:
            language = Language(
                name=line[3],
                normalized_name=line[3].lower().strip(),
                native_name=line[4]
            )

            language.save()


class Migration(migrations.Migration):
    dependencies = [
        ('std_bounties', '0006_auto_20180614_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('normalized_name', models.CharField(max_length=128)),
                ('native_name', models.CharField(max_length=128)),
            ],
        ),

        migrations.RunPython(add_languages),
    ]
