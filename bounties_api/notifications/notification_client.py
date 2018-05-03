from std_bounties.models import Fulfillment, Bounty
from notifications.models import Notification, NotificationDashboard
from notifications.constants import FULFILLMENT_SUBMITTED

class NotificationClient:
    def __init__(self):
        pass

    def fulfillment_submitted(self, bounty_id, fulfillment_id, timestamp):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(id=fulfillment_id)
        string_data = 'Fulfillment Submitted for: {}'.format(bounty.title)
        notification = Notification.objects.create(
            notification_id=FULFILLMENT_SUBMITTED,
            # user=TODO,
            notification_created=timestamp,
            email=True,
            dashboard=True
        )
        NotificationDashboard.objects.create(
            notification=notification,
            string_data=string_data
        )
        # Once we include email, email client call added here