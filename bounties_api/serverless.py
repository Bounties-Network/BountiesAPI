#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bounties.settings")

def run_manage_command(command):
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', command])

def resolve_blacklist(event):
    print('Starting manage.py for resolve_blacklist with event')
    print(event)
    run_manage_command('bounties_subscriber --blacklist')
