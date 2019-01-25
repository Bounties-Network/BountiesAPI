from activity.models import Activity, Object, Target
from activity.constants import activity_to_id


def generate_bounty_activity(activity_type, bounty, target):
    Activity.objects.create(
        actor=bounty.user,
        verb=activity_to_id[activity_type],
        object=Object.objects.get_or_create(bounty=bounty)[0],
        target=(Target.objects.get_or_create(target=target)[0] if target else None)
    )


def generate_fulfillment_activity(activity_type, fulfillment, target):
    Activity.objects.create(
        actor=fulfillment.user,
        verb=activity_to_id[activity_type],
        object=Object.objects.get_or_create(fulfillment=fulfillment)[0],
        target=(Target.objects.get_or_create(bounty=target)[0] if target else None)
    )


# draft activities
def draft_created(draft, target=None):
    generate_bounty_activity('DRAFT_CREATED', draft, target)


def draft_updated(draft, target=None):
    generate_bounty_activity('DRAFT_UPDATED', draft, target)


# bounty stage activities
def bounty_activated(bounty, target=None):
    generate_bounty_activity('BOUNTY_ACTIVATED', bounty, target)


def bounty_completed(bounty, target=None):
    generate_bounty_activity('BOUNTY_COMPLETED', bounty, target)


def bounty_expired(bounty, target=None):
    generate_bounty_activity('BOUNTY_EXPIRED', bounty, target)


def bounty_issued(bounty, target=None):
    generate_bounty_activity('BOUNTY_ISSUED', bounty, target)


def bounty_killed(bounty, target=None):
    generate_bounty_activity('BOUNTY_KILLED', bounty, target)


# bounty metadata activities
def bounty_contribution_added(bounty, target=None):
    generate_bounty_activity('BOUNTY_CONTRIBUTION_ADDED', bounty, target)


def bounty_deadline_extended(bounty, target=None):
    generate_bounty_activity('BOUNTY_DEADLINE_EXTENDED', bounty, target)


def bounty_payout_increased(bounty, target=None):
    generate_bounty_activity('BOUNTY_PAYOUT_INCREASED', bounty, target)


def bounty_transferred(bounty, target=None):
    generate_bounty_activity('BOUNTY_TRANSFERED', bounty, target)


# bounty comment activities
def bounty_comment_created(bounty, target=None):
    generate_bounty_activity('BOUNTY_COMMENT_CREATED', bounty, target)


# fulfillment activities
def fulfillment_accepted(fulfillment, target=None):
    generate_fulfillment_activity('FULFILLMENT_ACCEPTED', fulfillment, target)


def fulfillment_created(fulfillment, target=None):
    generate_fulfillment_activity('FULFILLMENT_CREATED', fulfillment, target)
