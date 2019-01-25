from activity.models import Activity, Target
from activity.constants import activity_to_id


def generate_bounty_activity(activity_type, bounty):
    Activity.objects.create(
        actor=bounty.user,
        verb=activity_to_id[activity_type],
        target=Target.objects.get_or_create(bounty=bounty)[0]
    )


def generate_fulfillment_activity(activity_type, fulfillment):
    Activity.objects.create(
        actor=fulfillment.user,
        verb=activity_to_id[activity_type],
        target=Target.objects.get_or_create(fulfillment=fulfillment)[0]
    )


# draft activities
def draft_created(draft):
    generate_bounty_activity('DRAFT_CREATED', draft)


def draft_updated(draft):
    generate_bounty_activity('DRAFT_UPDATED', draft)


# bounty stage activities
def bounty_activated(bounty):
    generate_bounty_activity('BOUNTY_ACTIVATED', bounty)


def bounty_completed(bounty):
    generate_bounty_activity('BOUNTY_COMPLETED', bounty)


def bounty_expired(bounty):
    generate_bounty_activity('BOUNTY_EXPIRED', bounty)


def bounty_issued(bounty):
    generate_bounty_activity('BOUNTY_ISSUED', bounty)


def bounty_killed(bounty):
    generate_bounty_activity('BOUNTY_KILLED', bounty)


# bounty metadata activities
def bounty_contribution_added(bounty):
    generate_bounty_activity('BOUNTY_CONTRIBUTION_ADDED', bounty)


def bounty_deadline_extended(bounty):
    generate_bounty_activity('BOUNTY_DEADLINE_EXTENDED', bounty)


def bounty_payout_increased(bounty):
    generate_bounty_activity('BOUNTY_PAYOUT_INCREASED', bounty)


def bounty_transferred(bounty):
    generate_bounty_activity('BOUNTY_TRANSFERED', bounty)


# bounty comment activities
def bounty_comment_created(bounty):
    generate_bounty_activity('BOUNTY_COMMENT_CREATED', bounty)


# fulfillment activities
def fulfillment_accepted(fulfillment):
    generate_fulfillment_activity('FULFILLMENT_ACCEPTED', fulfillment)


def fulfillment_created(fulfillment):
    generate_fulfillment_activity('FULFILLMENT_CREATED', fulfillment)
