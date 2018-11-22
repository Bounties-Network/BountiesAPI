#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bounties.settings")

def run_manage_command(manage_command):
    from django.core.management import execute_from_command_line
    manage_command.insert(0, 'runserver')
    execute_from_command_line(manage_command)

def resolve_blacklist(event, context):
    print('Starting manage.py for resolve_blacklist with event and context:')
    print(event)
    print(context)
    run_manage_command(['bounties_subscriber', '--blacklist'])
