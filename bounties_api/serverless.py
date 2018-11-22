#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bounties.settings")

def run_manage_command(command):
    from django.core.management import execute_from_command_line
    print('got command')
    print(command)
    execute_from_command_line(command.insert(0, 'manage.py'))

def resolve_blacklist(event, context):
    print('Starting manage.py for resolve_blacklist with event')
    print(event)
    print(context)
    run_manage_command(['bounties_subscriber', '--blacklist'])
