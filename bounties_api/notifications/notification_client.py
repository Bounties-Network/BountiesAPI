from std_bounties.models import Fulfillment, Bounty
from user.models import User
from notifications.constants import notifications
from notifications.notification_helpers import create_notification
from notifications.notification_templates import notification_templates, email_templates


class NotificationClient:
    def __init__(self):
        pass

    def bounty_issued(self, bounty_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyIssued'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyIssued'],
            bounty.user,
            bounty.bounty_created,
            string_data,
            'New bounty issued')

    def bounty_fulfilled(self, bounty_id, fulfillment_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(
            fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = notification_templates['FulfillmentSubmitted'].format(
            bounty_title=bounty.title)
        string_data_issuer = notification_templates['FulfillmentSubmittedIssuer'].format(
            bounty_title=bounty.title)
        # to fulfiller
        create_notification(
            bounty,
            str(uid) +
            str(notifications['FulfillmentSubmitted']),
            notifications['FulfillmentSubmitted'],
            fulfillment.user,
            fulfillment.fulfillment_created,
            string_data_fulfiller,
            'New Submission')
        # to bounty issuer
        create_notification(
            bounty,
            str(uid) +
            str(notifications['FulfillmentSubmittedIssuer']),
            notifications['FulfillmentSubmittedIssuer'],
            bounty.user,
            fulfillment.fulfillment_created,
            string_data_issuer,
            'You Received a New Submission',
            is_activity=False)

    def bounty_activated(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyActivated'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyActivated'],
            bounty.user,
            event_date,
            string_data,
            'Bounty Activated')

    def bounty_issued_and_activated(
            self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyActivated'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyIssuedActivated'],
            bounty.user,
            event_date,
            string_data,
            'Bounty Issued and Activated')

    def fulfillment_accepted(self, bounty_id, fulfillment_id, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(
            bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = notification_templates['FulfillmentAccepted'].format(
            bounty_title=bounty.title)
        string_data_fulfiller = notification_templates['FulfillmentAcceptedFulfiller'].format(
            bounty_title=bounty.title)
        string_data_issuer_email = email_templates['FulfillmentAccepted'].format(
            bounty_title=bounty.title)
        string_data_fulfiller_email = email_templates['FulfillmentAcceptedFulfiller'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            str(uid) + str(notifications['FulfillmentAccepted']),
            notifications['FulfillmentAccepted'],
            bounty.user,
            fulfillment.accepted_date,
            string_data_issuer,
            'Submission Accepted',
            string_data_email=string_data_issuer_email,
            email_button_string='Rate Fulfiller')
        create_notification(
            bounty,
            str(uid) +
            str(notifications['FulfillmentAcceptedFulfiller']),
            notifications['FulfillmentAcceptedFulfiller'],
            fulfillment.user,
            fulfillment.accepted_date,
            string_data_fulfiller,
            'Your Submission was Accepted',
            is_activity=False,
            string_data_email=string_data_fulfiller_email,
            email_button_string='Rate Issuer')

    def fulfillment_updated(
            self,
            bounty_id,
            fulfillment_id,
            event_date,
            uid,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(
            bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data_issuer = notification_templates['FulfillmentUpdatedIssuer'].format(
            bounty_title=bounty.title)
        string_data_fulfiller = notification_templates['FulfillmentUpdated'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            str(uid) +
            str(notifications['FulfillmentUpdatedIssuer']),
            notifications['FulfillmentUpdatedIssuer'],
            bounty.user,
            event_date,
            string_data_issuer,
            'Submission was Updated',
            is_activity=False)
        create_notification(
            bounty,
            str(uid) +
            str(notifications['FulfillmentUpdated']),
            notifications['FulfillmentUpdated'],
            fulfillment.user,
            event_date,
            string_data_fulfiller,
            'Submission Updated')

    def bounty_killed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyKilled'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyKilled'],
            bounty.user,
            event_date,
            string_data,
            'Bounty Killed')

    def contribution_added(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        amount = '{} {}'.format(
            bounty.tokenSymbol,
            bounty.calculated_fulfillmentAmount)
        string_data = notification_templates['ContributionAdded'].format(
            bounty_title=bounty.title, amount=amount)
        create_notification(
            bounty,
            uid,
            notifications['ContributionAdded'],
            bounty.user,
            event_date,
            string_data,
            'Contribution Added')

    def deadline_extended(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['DeadlineExtended'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['DeadlineExtended'],
            bounty.user,
            event_date,
            string_data,
            'Deadline Extended')

    def bounty_changed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyChanged'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyChanged'],
            bounty.user,
            event_date,
            string_data,
            'Bounty Updated')

    def issuer_transferred(
            self,
            bounty_id,
            transaction_from,
            inputs,
            event_date,
            uid,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        original_user = User.objects.get(public_address=transaction_from)
        string_data_transferrer = notification_templates['IssuerTransferred'].format(
            bounty_title=bounty.title)
        string_data_recipient = notification_templates['TransferRecipient'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            str(uid) +
            str(notifications['IssuerTransferred']),
            notifications['IssuerTransferred'],
            original_user,
            event_date,
            string_data_transferrer,
            'Bounty Transferred')
        create_notification(
            bounty,
            str(uid) +
            str(notifications['TransferRecipient']),
            notifications['TransferRecipient'],
            bounty.user,
            event_date,
            string_data_recipient,
            'A Bounty was Transferred to You',
            is_activity=False)

    def payout_increased(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['PayoutIncreased'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['PayoutIncreased'],
            bounty.user,
            event_date,
            string_data,
            'Payout Increased')

    def bounty_expired(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyExpired'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyExpired'],
            bounty.user,
            event_date,
            string_data,
            'Bounty Expired',
            is_activity=False)

    def comment_issued(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyComment'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['BountyComment'],
            bounty.user,
            event_date,
            string_data,
            'Your Bounty Received a Comment',
            is_activity=False)

    def rating_issued(self, bounty_id, event_date, uid, issuer, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['RatingIssued'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['RatingIssued'],
            issuer,
            event_date,
            string_data,
            'You Issued a New Rating')

    def rating_received(self, bounty_id, event_date, uid, receiver, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['RatingReceived'].format(
            bounty_title=bounty.title)
        create_notification(
            bounty,
            uid,
            notifications['RatingReceived'],
            receiver,
            event_date,
            string_data,
            'You Received a New Rating on Your Bounty',
            is_activity=False)
