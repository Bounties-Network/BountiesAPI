# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-11 15:14
from __future__ import unicode_literals

import json
from django.db import migrations, models

import os

def add_languages(apps, schema_editor):
    Language = apps.get_model('std_bounties', 'Language')

    print("the good shit ********************")
    print(os.getcwd())

    with open('./std_bounties/fixtures/languages.json') as f:
        languages_list = json.load(f)

        for language in languages_list:
            l = Language(name=language, normalized_name=language.lower().strip())
            l.save()


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
            ],
        ),

        migrations.RunPython(add_languages),
    ]
