from django.db.models import Q

from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.seo_client import SEOClient
from std_bounties.models import Bounty, Fulfillment
from activity import client as activity_client

bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackMessageClient()
seo_client = SEOClient()


# will be deprecated
def bounty_issued(bounty_id, **kwargs):
    bounty = Bounty.objects.filter(bounty_id=bounty_id)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('value', None)

    if bounty.exists():
        return

    created_bounty = bounty_client.issue_bounty(bounty_id, **kwargs)
    if not is_issue_and_activate:
        notification_client.bounty_issued(bounty_id, **kwargs)
        slack_client.bounty_issued(created_bounty)
        seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
        seo_client.publish_new_sitemap(created_bounty.platform)
        activity_client.bounty_issued(created_bounty)


def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.activate_bounty(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.bounty_activated(bounty)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('issuer', None)
    if is_issue_and_activate:
        seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
        seo_client.publish_new_sitemap(bounty.platform)
    # HOTFIX REMOVED
    #     slack_client.bounty_issued_and_activated(bounty)
    #     notification_client.bounty_issued_and_activated(bounty_id, **kwargs)
    # else:
    #     notification_client.bounty_activated(bounty_id, **kwargs)
    #     slack_client.bounty_activated(bounty)


def bounty_fulfilled(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.fulfill_bounty(bounty, **kwargs)
    fulfillment = Fulfillment.objects.get(
        Q(bounty__bounty_id=bounty.bounty_id),
        Q(fulfillment_id=fulfillment_id)
    )
    notification_client.bounty_fulfilled(bounty_id, **kwargs)
    slack_client.bounty_fulfilled(bounty, fulfillment_id)
    activity_client.fulfillment_created(fulfillment, bounty)


def fullfillment_updated(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.update_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_updated(bounty_id, **kwargs)
    slack_client.fulfillment_updated(bounty, fulfillment_id)


def fulfillment_accepted(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    fulfillment = Fulfillment.objects.get(
        Q(bounty__bounty_id=bounty.bounty_id),
        Q(fulfillment_id=fulfillment_id)
    )
    bounty_client.accept_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_accepted(bounty_id, **kwargs)
    slack_client.fulfillment_accepted(bounty, fulfillment_id)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.fulfillment_accepted(fulfillment, bounty)
    if bounty.balance < bounty.fulfillmentAmount:
        notification_client.bounty_completed(bounty, fulfillment_id)
        activity_client.bounty_completed(bounty)


def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.kill_bounty(bounty, **kwargs)
    notification_client.bounty_killed(bounty_id, **kwargs)
    slack_client.bounty_killed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.bounty_killed(bounty)


def contribution_added(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.add_contribution(bounty, **kwargs)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('issuer', None)
    if not is_issue_and_activate:
        seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
        activity_client.bounty_contribution_added(bounty)
    # HOTFIX REMOVED
    #     notification_client.contribution_added(bounty_id, **kwargs)
    #     slack_client.contribution_added(bounty)


def deadline_extended(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.extend_deadline(bounty, **kwargs)
    notification_client.deadline_extended(bounty_id, **kwargs)
    slack_client.deadline_extended(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.bounty_deadline_extended(bounty)


def bounty_changed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_bounty(bounty, **kwargs)
    notification_client.bounty_changed(bounty_id, **kwargs)
    slack_client.bounty_changed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)


def issuer_transferred(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.transfer_issuer(bounty, **kwargs)
    notification_client.issuer_transferred(bounty_id, **kwargs)
    slack_client.issuer_transferred(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.bounty_transferred(bounty)


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.increase_payout(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    activity_client.bounty_payout_increased(bounty)
    # HOTFIX REMOVED
    # notification_client.payout_increased(bounty_id, **kwargs)
    # slack_client.payout_increased(bounty)
