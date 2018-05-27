from std_bounties.models import Fulfillment, Bounty, BountyState, Event
from std_bounties.constants import ACTIVE_STAGE, EXPIRED_STAGE
from notifications.models import Notification, DashboardNotification
from notifications.constants import *
from notifications.notification_helpers import create_dashboard_notification
from notifications.notification_templates import *

class NotificationClient:
    def __init__(self):
        pass


    def bounty_issued(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ISSUED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ISSUED, bounty.user, bounty.bounty_created, string_data)


    def fulfillment_submitted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)
        # to fulfiller
        create_dashboard_notification(FULFILLMENT_SUBMITTED, fulfillment.user, fulfillment.fulfillment_created, string_data_fulfiller, is_activity=False)
        # to bounty issuer
        create_dashboard_notification(FULFILLMENT_SUBMITTED, bounty.user, fulfillment.fulfillment_created, string_data_issuer)
        # Once we include email, email client call added here


    def bounty_activated(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ACTIVATED, bounty.user, bounty_state.change_date, string_data)


    def bounty_issued_and_activated(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ISSUED_ACTIVATED, bounty.user, bounty_state.change_date, string_data)


    def fulfillment_accepted(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_ACCEPTED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_ACCEPTED_FULFILLER_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(FULFILLMENT_ACCEPTED, bounty.user, fulfillment.accepted_date, string_data_issuer)
        create_dashboard_notification(FULFILLMENT_ACCEPTED, fulfillment.user, fulfillment.accepted_date, string_data_fulfiller, is_activity=False)


    def fulfillment_updated(self, bounty_id, fulfillment_id, timestamp):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_UPDATED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_UPDATED_FULFILLER_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(FULFILLMENT_UPDATED, bounty.user, timestamp, string_data_issuer, is_activity=False)
        create_dashboard_notification(FULFILLMENT_UPDATED, fulfillment.user, timestamp, string_data_fulfiller, is_activity=False)


    def bounty_expired(self, bounty_id):
        bounty = Bounty.objects.get(id=bounty_id)
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=EXPIRED_STAGE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_EXPIRED, bounty.user, bounty_state.change_date, string_data)
