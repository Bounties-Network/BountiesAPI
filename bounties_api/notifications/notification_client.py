from std_bounties.models import Fulfillment, Bounty, BountyState
from notifications.models import Notification, NotificationDashboard
from notifications.constants import *
from notifications.notification_templates import *
from std_bounties.constants import EXPIRED, ACTIVE

class NotificationClient:
    def __init__(self):
        pass

    def fulfillment_submitted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)
        notification_fulfiller = Notification.objects.create(
            notification_id=FULFILLMENT_SUBMITTED,
            user=fulfillment.user,
            notification_created=fulfillment.fulfillment_created,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification_fulfiller,
            string_data=string_data_fulfiller
        )
        notification_issuer = Notification.objects.create(
            notification_id=FULFILLMENT_SUBMITTED,
            user=bounty.user,
            notification_created=fulfillment.fulfillment_created,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification_issuer,
            string_data=string_data_issuer
        )
        # Once we include email, email client call added here

    def bounty_activated(self, bounty_id):
        bounty = Bounty.objects.get(bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        notification = Notification.objects.create(
            notification_id=BOUNTY_ACTIVATED,
            user=bounty.user,
            notification_created=bounty_state.change_date,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification,
            string_data=string_data
        )


    def fulfillment_accepted(self, bounty_id, fulfillment_id):
        bounty = bounty.objects.get(id=bounty_id)
        fulfillment = fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data = FULFILLMENT_ACCEPTED_STR.format(bounty_title=bounty_title)
        notification = Notification.objects.create(
            notification_id=FULFILLMENT_ACCEPTED,
            user=bounty.user,
            notification_created=fulfillment.accepted_date,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification,
            string_data=string_data
        )


    def bounty_expired(self, bounty_id):
        bounty = bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty_title)
        notification = Notification.objects.create(
            notification_id=BOUNTY_EXPIRED,
            user=bounty.user,
            notification_created=bounty_state.change_date,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification,
            string_data=string_data
        )
