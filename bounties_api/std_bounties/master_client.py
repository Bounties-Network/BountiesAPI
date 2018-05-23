from decimal import Decimal
from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.client_helpers import bounty_url_for
from std_bounties.models import Bounty
from bounties.ses_client import send_email


bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackMessageClient()


def bounty_issued(bounty_id, **kwargs):
    bounty = Bounty.objects.filter(bounty_id=bounty_id)

    if not bounty.exists():
        created_bounty = bounty_client.issue_bounty(bounty_id, **kwargs)
        slack_client.bounty_issued(created_bounty)


def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.activate_bounty(bounty, **kwargs)
    notification_client.bounty_activated(bounty_id)
    slack_client.bounty_activated(bounty)


def bounty_fulfilled(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.fulfill_bounty(bounty, **kwargs)
    notification_client.fulfillment_submitted(bounty_id, fulfillment_id)
    slack_client.bounty_fulfilled(bounty, fulfillment_id)

    if bounty.platform == 'colorado':
        email_url = bounty_url_for(bounty_id, platform='colorado')
    else:
        email_url = bounty_url_for(bounty_id)

    if bounty.platform != 'gitcoin':
        send_email(bounty.issuer_email, 'Bounty Contribution Received',
            'Hey there! You received a contribution for your bounty: {}. {}'.format(bounty.title, email_url))


def fullfillment_updated(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.update_fulfillment(bounty, **kwargs)
    slack_client.fulfillment_updated(bounty, fulfillment_id)


def fulfillment_accepted(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.accept_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_accepted(bounty_id, fulfillment_id)
    slack_client.fulfillment_accepted(bounty, fulfillment_id)


def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.kill_bounty(bounty, **kwargs)
    slack_client.bounty_killed(bounty)


def contribution_added(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.add_contribution(bounty, **kwargs)
    slack_client.contribution_added(bounty)


def deadline_extended(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.extend_deadline(bounty, **kwargs)
    slack_client.deadline_extended(bounty)


def bounty_changed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_bounty(bounty, **kwargs)
    slack_client.bounty_changed(bounty)


def issuer_transfered(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.transfer_issuer(bounty, **kwargs)
    slack_client.issuer_transfered(bounty)


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.increase_payout(bounty, **kwargs)
    slack_client.payout_increased(bounty)

