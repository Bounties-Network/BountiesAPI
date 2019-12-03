from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.seo_client import SEOClient
from std_bounties.models import Bounty, Fulfillment, Activity, User
from std_bounties.constants import STANDARD_BOUNTIES_V1


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
    @keyword token_contract
    @keyword token_version
    @keyword transaction_hash
    """

    if Bounty.objects.filter(
            bounty_id=bounty_id,
            contract_version=contract_version
    ).exists():
        return

    created_bounty = bounty_client.issue_bounty(
        bounty_id,
        contract_version,
        **kwargs
    )
    Activity.objects.get_or_create(
        bounty_id=created_bounty.id,
        event_type='BountyIssued',
        user_id=created_bounty.user_id,
        defaults={
            'event_type': 'BountyIssued',
            'bounty_id': created_bounty.id,
            'user_id': created_bounty.user_id,
            'community_id': created_bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': created_bounty.created
        }
    )
    notification_client.bounty_issued(created_bounty, **kwargs)
    slack_client.bounty_issued(created_bounty)
    seo_client.bounty_preview_screenshot(created_bounty.platform, bounty_id, contract_version)
    seo_client.publish_new_sitemap(created_bounty.platform)


@export
def contribution_added(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword contribution_id
    @keyword contributor
    @keyword amount
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    contribution = bounty_client.add_contribution(bounty, **kwargs)

    # only create notifications if it isn't the first contribution
    if int(kwargs.get('contribution_id')) != 0:
        Activity.objects.get_or_create(
            bounty_id=bounty.id,
            event_type='ContributionAdded',
            user_id=contribution.contributor_id,
            defaults={
                'event_type': 'ContributionAdded',
                'bounty_id': bounty.id,
                'user_id': contribution.contributor_id,
                'community_id': bounty.community_id,
                'transaction_hash': kwargs.get('transaction_hash'),
                'date': bounty.created
            }
        )
        seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)
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
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    contribution = bounty_client.refund_contribution(bounty, **kwargs)


@export
def action_performed(bounty_id, contract_version, **kwargs):
    """
    Perform an arbitrary action on a bounty
    @param bounty_id
    @param contract_version
    @keyword fulfiller
    @keyword data
    @keyword transaction_hash
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
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    fulfillment = bounty_client.fulfill_bounty(bounty, **kwargs)

    fulfillment_id = kwargs.get('fulfillment_id')
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        fulfillment_id=fulfillment.id,
        event_type='BountyFulfilled',
        user_id=fulfillment.user_id,
        defaults={
            'event_type': 'BountyFulfilled',
            'bounty_id': bounty.id,
            'fulfillment_id': fulfillment.id,
            'user_id': fulfillment.user_id,
            'community_id': fulfillment.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': fulfillment.fulfillment_created
        }
    )
    notification_client.bounty_fulfilled(bounty, fulfillment, **kwargs)
    slack_client.bounty_fulfilled(bounty, fulfillment_id)


@export
def fulfillment_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword fulfillment_id
    @keyword fulfillers
    @keyword data
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    fulfillment = bounty_client.update_fulfillment(bounty, **kwargs)

    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        fulfillment_id=fulfillment.id,
        event_type='FulfillmentUpdated',
        user_id=fulfillment.user_id,
        defaults={
            'event_type': 'FulfillmentUpdated',
            'bounty_id': bounty.id,
            'fulfillment_id': fulfillment.id,
            'user_id': fulfillment.user_id,
            'community_id': fulfillment.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': fulfillment.fulfillment_created
        }
    )

    fulfillment_id = kwargs.get('fulfillment_id')
    notification_client.fulfillment_updated(bounty, **kwargs)
    slack_client.fulfillment_updated(bounty, fulfillment_id)


@export
def fulfillment_accepted(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword fulfillment_id
    @keyword approver
    @keyword token_amounts
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    fulfillment = bounty_client.accept_fulfillment(bounty, **kwargs)

    fulfillment_id = kwargs.get('fulfillment_id')

    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        fulfillment_id=fulfillment.id,
        event_type='FulfillmentAccepted',
        user_id=bounty.user_id,
        defaults={
            'event_type': 'FulfillmentAccepted',
            'bounty_id': bounty.id,
            'fulfillment_id': fulfillment.id,
            'user_id': bounty.user_id,
            'community_id': fulfillment.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': fulfillment.fulfillment_created
        }
    )

    notification_client.fulfillment_accepted(bounty, fulfillment, **kwargs)
    slack_client.fulfillment_accepted(bounty, fulfillment_id)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)

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
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.change_bounty(bounty, **kwargs)
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyChanged',
        user_id=bounty.user_id,
        defaults={
            'event_type': 'BountyChanged',
            'bounty_id': bounty.id,
            'user_id': bounty.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    notification_client.bounty_changed(bounty, **kwargs)
    slack_client.bounty_changed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


@export
def bounty_data_changed(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword data
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.change_data(bounty, **kwargs)
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyDataChanged',
        user_id=bounty.user_id,
        defaults={
            'event_type': 'BountyDataChanged',
            'bounty_id': bounty.id,
            'user_id': bounty.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    notification_client.bounty_changed(bounty, **kwargs)
    slack_client.bounty_changed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


@export
def bounty_issuers_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword issuers
    @keyword changer
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty = bounty_client.update_bounty_issuers(bounty, **kwargs)
    changer = User.objects.get(public_address=kwargs.get('transaction_hash'))
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyIssuersUpdated',
        user_id=changer.user_id,
        defaults={
            'event_type': 'BountyIssuersUpdated',
            'bounty_id': bounty.id,
            'user_id': changer.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


@export
def bounty_approvers_updated(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword approvers
    @keyword changer
    @keyword transaction_hash
    """
    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.update_bounty_approvers(bounty, **kwargs)
    changer = User.objects.get(public_address=kwargs.get('transaction_hash'))
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyApproversUpdated',
        user_id=changer.user_id,
        defaults={
            'event_type': 'BountyApproversUpdated',
            'bounty_id': bounty.id,
            'user_id': changer.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


@export
def bounty_deadline_changed(bounty_id, contract_version, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword deadline
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.change_deadline(bounty, **kwargs)

    changer = User.objects.get(public_address=kwargs.get('transaction_hash'))
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyDeadlineChanged',
        user_id=changer.user_id,
        defaults={
            'event_type': 'BountyDeadlineChanged',
            'bounty_id': bounty.id,
            'user_id': changer.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    notification_client.deadline_changed(bounty, **kwargs)
    slack_client.deadline_extended(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


# will be deprecated
@export
def bounty_activated(bounty_id, **kwargs):
    """
    @param bounty_id
    @param contract_version
    @keyword changer
    @keyword deadline
    @keyword transaction_hash
    """
    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=STANDARD_BOUNTIES_V1)
    bounty_client.activate_bounty(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, 1)

    # HOTFIX REMOVED
    #     slack_client.bounty_issued_and_activated(bounty)
    #     notification_client.bounty_issued_and_activated(bounty_id, **kwargs)
    # else:
    #     notification_client.bounty_activated(bounty_id, **kwargs)
    #     slack_client.bounty_activated(bounty)


# legacy
@export
def bounty_killed(bounty_id, contract_version, **kwargs):
    '''
    @param bounty_id
    @param contract_version
    @keyword transaction_hash
    '''

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=STANDARD_BOUNTIES_V1)
    bounty_client.kill_bounty(bounty, **kwargs)
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyKilled',
        user_id=bounty.user_id,
        defaults={
            'event_type': 'BountyKilled',
            'bounty_id': bounty.id,
            'user_id': bounty.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    notification_client.bounty_killed(bounty_id, **kwargs)
    slack_client.bounty_killed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, STANDARD_BOUNTIES_V1)


@export
def bounty_drained(bounty_id, contract_version, **kwargs):

    """
    @param bounty_id
    @param contract_version
    @keyword amounts
    @keyword transaction_hash
    """

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.kill_bounty(bounty, **kwargs)
    Activity.objects.get_or_create(
        bounty_id=bounty.id,
        event_type='BountyDrained',
        user_id=bounty.user_id,
        defaults={
            'event_type': 'BountyDrained',
            'bounty_id': bounty.id,
            'user_id': bounty.user_id,
            'community_id': bounty.community_id,
            'transaction_hash': kwargs.get('transaction_hash'),
            'date': bounty.modified
        }
    )
    slack_client.bounty_killed(bounty)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)


@export
def payout_increased(bounty_id, contract_version, **kwargs):
    '''
    @param bounty_id
    @param contract_version
    @keyword fulfillment_amount
    @keyword transaction_hash
    '''

    bounty = Bounty.objects.get(bounty_id=bounty_id, contract_version=contract_version)
    bounty_client.increase_payout(bounty, **kwargs)
    seo_client.bounty_preview_screenshot(bounty.platform, bounty_id, contract_version)

    # HOTFIX REMOVED
    # notification_client.payout_increased(bounty_id, **kwargs)
    # slack_client.payout_increased(bounty)
