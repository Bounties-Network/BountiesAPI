from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.seo_client import SEOClient
from std_bounties.models import Bounty, Fulfillment


bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackMessageClient()
seo_client = SEOClient()

client = {}


def export(f):
    client.setdefault(f.__name__, f)


@export
def bounty_issued(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword creator
    @keyword issuers
    @keyword approvers
    @keyword data
    @keyword deadline
    @keyword token
    @keyword token_version
    """

    if Bounty.objects.filter(bounty_id=bounty_id).exists():
        return

    created_bounty = bounty_client.issue_bounty(
        bounty_id,
        contract_version,
        **kwargs
    )

    notification_client.bounty_issued(created_bounty, **kwargs)
    slack_client.bounty_issued(created_bounty)
    seo_client.bounty_preview_screenshot(created_bounty.platform, bounty_id)
    seo_client.publish_new_sitemap(created_bounty.platform)


@export
def contribution_added(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword contribution_id
    @keyword contributor
    @keyword amount
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    contribution = bounty_client.add_contribution(bounty, **kwargs)

    # only create notifications if it isn't the first contribution
    if int(kwargs.get('contribution_id')) != 0:
        seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
        notification_client.contribution_added(contribution, **kwargs)
        slack_client.contribution_added(bounty)


@export
def contribution_refunded(bounty_id, contract_version, **kwargs):
    """
    Refund a contribution
    @param bounty_id
    @param contract_version
    @keyword bounty_id
    @keyword contribution_id
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.refund_contribution(bounty, **kwargs)


@export
def action_performed(bounty_id, contract_version, **kwargs):
    """
    Perform an arbitrary action on a bounty
    @param bounty_id
    @param contract_version
    @keyword fulfiller
    @keyword data
    """

    # this will need to be implemented on a case-by-case basis

    pass


@export
def bounty_fulfilled(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword fulfillment_id
    @keyword fulfillers
    @keyword data
    @keyword submitter
    """

    fulfillment = Fulfillment.objects.filter(
        fulfillment_id=kwargs.get('fulfillment_id'),
        bounty_id=bounty_id,
        contract_version=contract_version
    )

    if fulfillment.exists():
        return

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    fulfillment = bounty_client.fulfill_bounty(bounty, **kwargs)

    fulfillment_id = kwargs.get('fulfillment_id')
    notification_client.bounty_fulfilled(bounty, fulfillment, **kwargs)
    slack_client.bounty_fulfilled(bounty, fulfillment_id)


@export
def fullfillment_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword fulfillment_id
    @keyword fulfillers
    @keyword data
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.update_fulfillment(bounty, **kwargs)

    fulfillment_id = kwargs.get('fulfillment_id')
    notification_client.fulfillment_updated(bounty_id, **kwargs)
    slack_client.fulfillment_updated(bounty, fulfillment_id)


@export
def fulfillment_accepted(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword fulfillment_id
    @keyword approver
    @keyword token_amounts
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    fulfillment = bounty_client.accept_fulfillment(bounty, **kwargs)

    fulfillment_id = kwargs.get('fulfillment_id')

    notification_client.fulfillment_accepted(bounty, fulfillment, **kwargs)
    slack_client.fulfillment_accepted(bounty, fulfillment_id)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)

    if bounty.balance < bounty.fulfillment_amount:
        notification_client.bounty_completed(bounty, fulfillment_id)


@export
def bounty_changed(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword issuers
    @keyword approvers
    @keyword data
    @keyword deadline
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_bounty(bounty, **kwargs)
    notification_client.bounty_changed(bounty, **kwargs)
    slack_client.bounty_changed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)


@export
def bounty_data_changed(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword data
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_data(bounty, **kwargs)


@export
def bounty_issuers_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword issuers
    @keyword changer
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty = bounty_client.update_issuers(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty)


def bounty_approvers_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword approvers
    @keyword changer
    """
    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.change_bounty_approver(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty)


@export
def bounty_deadline_changed(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword deadline
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.change_deadline(bounty, **kwargs)

    notification_client.deadline_changed(bounty, **kwargs)
    slack_client.deadline_extended(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)


# will be deprecated
def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.activate_bounty(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
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


# legacy
def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.kill_bounty(bounty, **kwargs)
    notification_client.bounty_killed(bounty_id, **kwargs)
    slack_client.bounty_killed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)


def issuer_transferred(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.transfer_issuer(bounty, **kwargs)
    notification_client.issuer_transferred(bounty_id, **kwargs)
    slack_client.issuer_transferred(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.increase_payout(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id)
    # HOTFIX REMOVED
    # notification_client.payout_increased(bounty_id, **kwargs)
    # slack_client.payout_increased(bounty)
