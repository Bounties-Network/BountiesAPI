from std_bounties.models import Fulfillment, Bounty, BountyState, Event
from std_bounties.constants import ACTIVE_STAGE, EXPIRED_STAGE
from notifications.models import Notification, DashboardNotification
from notifications.constants import *
from notifications.notification_helpers import create_dashboard_notification
from notifications.notification_templates import *

class NotificationClient:
    def __init__(self):
        pass


    def bounty_issued(self, bounty_id, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ISSUED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ISSUED, bounty.user, bounty.bounty_created, string_data)


    def bounty_fulfilled(self, bounty_id, fulfillment_id, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)
        # to fulfiller
        create_dashboard_notification(FULFILLMENT_SUBMITTED, fulfillment.user, fulfillment.fulfillment_created, string_data_fulfiller, is_activity=False)
        # to bounty issuer
        create_dashboard_notification(FULFILLMENT_SUBMITTED, bounty.user, fulfillment.fulfillment_created, string_data_issuer)
        # Once we include email, email client call added here


    def bounty_activated(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ACTIVATED, bounty.user, event_date, string_data)


    def bounty_issued_and_activated(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_ISSUED_ACTIVATED, bounty.user, event_date, string_data)


    def fulfillment_accepted(self, bounty_id, fulfillment_id, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_ACCEPTED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_ACCEPTED_FULFILLER_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(FULFILLMENT_ACCEPTED, bounty.user, fulfillment.accepted_date, string_data_issuer)
        create_dashboard_notification(FULFILLMENT_ACCEPTED, fulfillment.user, fulfillment.accepted_date, string_data_fulfiller, is_activity=False)


    def fulfillment_updated(self, bounty_id, fulfillment_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_UPDATED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_UPDATED_FULFILLER_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(FULFILLMENT_UPDATED, bounty.user, event_date, string_data_issuer, is_activity=False)
        create_dashboard_notification(FULFILLMENT_UPDATED, fulfillment.user, event_date, string_data_fulfiller, is_activity=False)


    def bounty_killed(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_KILLED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_KILLED, bounty.user, event_date, string_data)


    def contribution_added(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        amount = '{} {}'.format(bounty.tokenSymbol, bounty.calculated_fulfillmentAmount)
        string_data = CONTRIBUTION_ADDED_STR.format(bounty_title=bounty.title, amount=amount)
        create_dashboard_notification(CONTRIBUTION_ADDED, bounty.user, event_date, string_data)


    def deadline_extended(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = DEADLINE_EXTENDED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(DEADLINE_EXTENDED, bounty.user, event_date, string_data)


    def bounty_changed(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_CHANGED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_CHANGED, bounty.user, event_date, string_data)


    def issuer_transferred(self, bounty_id, transaction_from, inputs, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        original_user = User.objects.get(public_address=transaction_from)
        string_data_transferrer = ISSUER_TRANSFERRED_STR.format(bounty_title=bounty.title)
        string_data_recipient = ISSUER_TRANSFERRED_RECIPIENT_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(ISSUER_TRANSFERRED, original_user, event_date, string_data_transferrer)
        create_dashboard_notification(TRANSFER_RECIPIENT, bounty.user, event_date, string_data_recipient)


    def payout_increased(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = PAYOUT_INCREASED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(PAYOUT_INCREASED, bounty.user, event_date, string_data)


    def bounty_expired(self, bounty_id, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        create_dashboard_notification(BOUNTY_EXPIRED, bounty.user, event_date, string_data)
