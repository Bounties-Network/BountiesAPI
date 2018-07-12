from std_bounties.models import Fulfillment, Bounty, BountyState, Event
from std_bounties.constants import ACTIVE_STAGE, EXPIRED_STAGE
from notifications.models import Notification, DashboardNotification
from user.models import User
from notifications.constants import *
from notifications.notification_helpers import create_notification
from notifications.notification_templates import *

class NotificationClient:
    def __init__(self):
        pass


    def bounty_issued(self, bounty_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ISSUED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_ISSUED, bounty.user, bounty.bounty_created, string_data, 'New bounty issued')


    def bounty_fulfilled(self, bounty_id, fulfillment_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)
        # to fulfiller
        create_notification(bounty, str(uid) + str(FULFILLMENT_SUBMITTED), FULFILLMENT_SUBMITTED, fulfillment.user, fulfillment.fulfillment_created, string_data_fulfiller, 'New Submission')
        # to bounty issuer
        create_notification(bounty, str(uid) + str(FULFILLMENT_SUBMITTED_ISSUER), FULFILLMENT_SUBMITTED_ISSUER, bounty.user, fulfillment.fulfillment_created, string_data_issuer, 'You Received a New Submission', is_activity=False)


    def bounty_activated(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_ACTIVATED, bounty.user, event_date, string_data, 'Bounty Activated')


    def bounty_issued_and_activated(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_ISSUED_ACTIVATED, bounty.user, event_date, string_data, 'Bounty Issued and Activated')


    def fulfillment_accepted(self, bounty_id, fulfillment_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_ACCEPTED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_ACCEPTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer_email = FULFILLMENT_ACCEPTED_ISSUER_EMAIL.format(bounty_title=bounty.title)
        string_data_fulfiller_email = FULFILLMENT_ACCEPTED_FULFILLER_EMAIL.format(bounty_title=bounty.title)
        create_notification(bounty, str(uid) + str(FULFILLMENT_ACCEPTED), FULFILLMENT_ACCEPTED, bounty.user, fulfillment.accepted_date, string_data_issuer, 'Submission Accepted', string_data_email=string_data_issuer_email, email_button_string='Rate Fulfiller')
        create_notification(bounty, str(uid) + str(FULFILLMENT_ACCEPTED_FULFILLER), FULFILLMENT_ACCEPTED_FULFILLER, fulfillment.user, fulfillment.accepted_date, string_data_fulfiller, 'Your Submission was Accepted', is_activity=False, string_data_email=string_data_fulfiller_email, email_button_string='Rate Issuer')


    def fulfillment_updated(self, bounty_id, fulfillment_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = FULFILLMENT_UPDATED_ISSUER_STR.format(bounty_title=bounty.title)
        string_data_fulfiller = FULFILLMENT_UPDATED_FULFILLER_STR.format(bounty_title=bounty.title)
        create_notification(bounty, str(uid) + str(FULFILLMENT_UPDATED_ISSUER), FULFILLMENT_UPDATED_ISSUER, bounty.user, event_date, string_data_issuer, 'Submission was Updated', is_activity=False)
        create_notification(bounty, str(uid) + str(FULFILLMENT_UPDATED), FULFILLMENT_UPDATED, fulfillment.user, event_date, string_data_fulfiller, 'Submission Updated')


    def bounty_killed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_KILLED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_KILLED, bounty.user, event_date, string_data, 'Bounty Killed')


    def contribution_added(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        amount = '{} {}'.format(bounty.tokenSymbol, bounty.calculated_fulfillmentAmount)
        string_data = CONTRIBUTION_ADDED_STR.format(bounty_title=bounty.title, amount=amount)
        create_notification(bounty, uid, CONTRIBUTION_ADDED, bounty.user, event_date, string_data, 'Contribution Added')


    def deadline_extended(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = DEADLINE_EXTENDED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, DEADLINE_EXTENDED, bounty.user, event_date, string_data, 'Deadline Extended')


    def bounty_changed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_CHANGED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_CHANGED, bounty.user, event_date, string_data, 'Bounty Updated')


    def issuer_transferred(self, bounty_id, transaction_from, inputs, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        original_user = User.objects.get(public_address=transaction_from)
        string_data_transferrer = ISSUER_TRANSFERRED_STR.format(bounty_title=bounty.title)
        string_data_recipient = ISSUER_TRANSFERRED_RECIPIENT_STR.format(bounty_title=bounty.title)
        create_notification(bounty, str(uid) + str(ISSUER_TRANSFERRED), ISSUER_TRANSFERRED, original_user, event_date, string_data_transferrer, 'Bounty Transferred')
        create_notification(bounty, str(uid) + str(TRANSFER_RECIPIENT), TRANSFER_RECIPIENT, bounty.user, event_date, string_data_recipient, 'A Bounty was Transferred to You', is_activity=False)


    def payout_increased(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = PAYOUT_INCREASED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, PAYOUT_INCREASED, bounty.user, event_date, string_data, 'Payout Increased')


    def bounty_expired(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_EXPIRED, bounty.user, event_date, string_data, 'Bounty Expired', is_activity=False)


    def comment_issued(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = BOUNTY_COMMENT_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, BOUNTY_COMMENT, bounty.user, event_date, string_data, 'Your Bounty Received a Comment', is_activity=False)


    def rating_issued(self, bounty_id, event_date, uid, issuer, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = RATING_ISSUE_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, RATING_ISSUED, issuer, event_date, string_data, 'You Issued a New Rating')


    def rating_received(self, bounty_id, event_date, uid, receiver, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = RATING_RECEIVED_STR.format(bounty_title=bounty.title)
        create_notification(bounty, uid, RATING_RECEIVED, receiver, event_date, string_data, 'You Received a New Rating on Your Bounty', is_activity=False)
