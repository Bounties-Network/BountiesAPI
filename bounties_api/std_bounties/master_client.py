from functools import partial, update_wrapper
from decimal import Decimal

from bounties import settings
from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.client_helpers import bounty_url_for, apply_and_notify, formatted_fulfillment_amount, token_price, format_deadline, usd_price, token_lock_price
from std_bounties.models import Bounty
from utils.functional_tools import merge, narrower, wrapped_partial

from slackclient import SlackClient


bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackClient(settings.SLACK_TOKEN)


# @with_clients
def bounty_issued(bounty_id, **kwargs):
    bounty = Bounty.objects.filter(bounty_id=bounty_id)

    if not bounty.exists():
        bounty_client.issue_bounty(bounty_id, **kwargs)
        slack_client.issue_bounty(bounty, **kwargs)


# @with_clients
def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.activate_bounty(bounty, **kwargs)
    notification_client.bounty_activated(bounty)
    slack_client.bounty_activated(bounty)


# @with_clients
def bounty_fulfilled(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.fulfill_bounty(bounty, **kwargs)
    notification_client.fulfillment_submitted(bounty, kwargs.get('fulfillment_id'))
    notification_client.fulfillment_submitted(bounty, kwargs.get('fulfillment_id'))


def fullfillment_updated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.update_fulfillment(bounty, **kwargs)
    slack_client.update_fulfillment(bounty, **kwargs)


def fulfillment_accepted(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.accept_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_accepted(bounty, kwargs.get('fulfillment_id'))
    slack_client.fulfillment_accepted(bounty, kwargs.get('fulfillment_id'))


def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.kill_bounty(bounty, **kwargs)
    slack_client.kill_bounty(bounty, **kwargs)


def contribution_added(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.add_contribution(bounty, **kwargs)
    slack_client.kill_bounty(bounty, **kwargs)


def deadline_extended(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.extend_deadline(bounty, **kwargs)
    slack_client.extend_deadline(bounty, **kwargs)


def bounty_changed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_bounty(bounty, **kwargs)
    slack_client.change_bounty(bounty, **kwargs)


def issuer_transfered(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.transfer_issuer(bounty, **kwargs)
    slack_client.transfer_issuer(bounty, **kwargs)


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.increase_payout(bounty, **kwargs)
    slack_client.increase_payout(bounty, **kwargs)