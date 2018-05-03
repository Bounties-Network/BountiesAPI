from std_bounties.models import Fulfillment, Bounty
from notifications.models import Notification, NotificationDashboard
from notifications.constants import FULFILLMENT_SUBMITTED
from notifications.notification_templates import *

class NotificationClient:
    def __init__(self):
        pass

    def fulfillment_submitted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(id=fulfillment_id)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER.format(bounty_title=bounty.title)
        notification_fulfiller = Notification.objects.create(
            notification_id=FULFILLMENT_SUBMITTED,
            fulfillment.user,
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
            fulfillment.user,
            notification_created=fulfillment.fulfillment_created,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification_issuer,
            string_data=string_data_issuer
        )
        # Once we include email, email client call added here

    def bounty_submitted(self, bounty_id):
        pass

    def fulfillment_accepted(self, bounty_id, fulfillment_id):
        pass

    def bounty_expired(self, bounty_id):
        pass
