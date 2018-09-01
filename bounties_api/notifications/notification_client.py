from datetime import datetime
from std_bounties.models import Fulfillment, Bounty, Comment
from user.models import User
from notifications.constants import notifications
from notifications.notification_helpers import (
    create_bounty_notification,
    create_profile_updated_notification
)
from notifications.notification_templates import (
    notification_templates,
    email_templates
)


class NotificationClient:
    def __init__(self):
        pass

    def bounty_issued(self, bounty_id, uid, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyIssued'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyIssued'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='New bounty issued')

    def bounty_fulfilled(self, bounty_id, fulfillment_id, uid, event_date, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        fulfillment = Fulfillment.objects.get(
            fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = notification_templates['FulfillmentSubmitted'].format(
            bounty_title=bounty.title)
        string_data_issuer = notification_templates['FulfillmentSubmittedIssuer'].format(
            bounty_title=bounty.title)
        # to fulfiller
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['FulfillmentSubmitted']),
            notification_name=notifications['FulfillmentSubmitted'],
            user=fulfillment.user,
            from_user=bounty.user,
            string_data=string_data_fulfiller,
            notification_created=event_date,
            subject='New Submission')
        # to bounty issuer
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['FulfillmentSubmittedIssuer']),
            notification_name=notifications['FulfillmentSubmittedIssuer'],
            user=bounty.user,
            from_user=fulfillment.user,
            string_data=string_data_issuer,
            subject='You Received a New Submission',
            description=fulfillment.description,
            notification_created=event_date,
            is_activity=False)

    def bounty_activated(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyActivated'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyActivated'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Bounty Activated')

    def bounty_issued_and_activated(
            self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyActivated'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyIssuedActivated'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Bounty Issued and Activated')

    def fulfillment_accepted(self, bounty_id, fulfillment_id, uid, event_date, **kwargs):
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
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['FulfillmentAccepted']),
            notification_name=notifications['FulfillmentAccepted'],
            user=bounty.user,
            from_user=fulfillment.user,
            string_data=string_data_issuer,
            subject='Submission Accepted',
            string_data_email=string_data_issuer_email,
            notification_created=event_date,
            email_button_string='Rate Fulfiller')
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['FulfillmentAcceptedFulfiller']),
            notification_name=notifications['FulfillmentAcceptedFulfiller'],
            user=fulfillment.user,
            from_user=bounty.user,
            string_data=string_data_fulfiller,
            subject='Your Submission was Accepted',
            is_activity=False,
            string_data_email=string_data_fulfiller_email,
            notification_created=event_date,
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
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['FulfillmentUpdatedIssuer']),
            notification_name=notifications['FulfillmentUpdatedIssuer'],
            user=bounty.user,
            from_user=fulfillment.user,
            string_data=string_data_issuer,
            subject='Submission was Updated',
            notification_created=event_date,
            is_activity=False)
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) +
            str(notifications['FulfillmentUpdated']),
            notification_name=notifications['FulfillmentUpdated'],
            user=fulfillment.user,
            from_user=bounty.user,
            string_data=string_data_fulfiller,
            notification_created=event_date,
            subject='Submission Updated')

    def bounty_killed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyKilled'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyKilled'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Bounty Killed')

    def contribution_added(
            self,
            bounty_id,
            event_date,
            inputs,
            transaction_from,
            uid,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        amount = '{} {}'.format(
            bounty.tokenSymbol,
            bounty.calculated_fulfillmentAmount)
        string_data = notification_templates['ContributionAdded'].format(
            bounty_title=bounty.title, amount=amount)
        from_user = transaction_from and User.objects.get(
            public_address=transaction_from.lower())
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['ContributionAdded'],
            user=bounty.user,
            from_user=from_user,
            string_data=string_data,
            notification_created=event_date,
            inputs=inputs,
            subject='Contribution Added')

    def deadline_extended(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['DeadlineExtended'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['DeadlineExtended'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Deadline Extended')

    def bounty_changed(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyChanged'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyChanged'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Bounty Updated')

    def issuer_transferred(
            self,
            bounty_id,
            transaction_from,
            inputs,
            event_date,
            uid,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        original_user = User.objects.get(
            public_address=transaction_from.lower())
        string_data_transferrer = notification_templates['IssuerTransferred'].format(
            bounty_title=bounty.title)
        string_data_recipient = notification_templates['TransferredRecipient'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['IssuerTransferred']),
            notification_name=notifications['IssuerTransferred'],
            user=original_user,
            from_user=bounty.user,
            string_data=string_data_transferrer,
            notification_created=event_date,
            subject='Bounty Transferred')
        create_bounty_notification(
            bounty=bounty,
            uid=str(uid) + str(notifications['TransferRecipient']),
            notification_name=notifications['TransferRecipient'],
            user=bounty.user,
            from_user=original_user,
            string_data=string_data_recipient,
            subject='A Bounty was Transferred to You',
            notification_created=event_date,
            is_activity=False)

    def payout_increased(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['PayoutIncreased'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['PayoutIncreased'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            notification_created=event_date,
            subject='Payout Increased')

    def bounty_expired(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['BountyExpired'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid=uid,
            notification_name=notifications['BountyExpired'],
            user=bounty.user,
            from_user=None,
            string_data=string_data,
            subject='Bounty Expired',
            notification_created=event_date,
            is_activity=False)

    def comment_issued(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        comment = Comment.objects.get(id=uid)
        string_data = notification_templates['BountyComment'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid='BountyComment' + str(uid),
            notification_name=notifications['BountyComment'],
            user=comment.user,
            from_user=None,
            string_data=string_data,
            subject='You Commented on a Bounty',
            notification_created=event_date,
            is_activity=True)

    def comment_received(self, bounty_id, event_date, uid, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        comment = Comment.objects.get(id=uid)
        string_data = notification_templates['BountyCommentReceived'].format(
            bounty_title=bounty.title)

        users = list(filter(
            lambda u: u != bounty.issuer and u != comment.user,
            map(lambda c: c.user, bounty.comments.all())))

        if bounty.issuer != comment.user:
            users.append(bounty.issuer)

        for user in set(users):
            create_bounty_notification(
                bounty=bounty,
                uid='{}-{}'.format(uid, user.id),
                notification_name=notifications['BountyCommentReceived'],
                user=user,
                from_user=comment.user,
                string_data=string_data,
                subject='Your Bounty Received a Comment',
                notification_created=event_date,
                comment=comment,
                is_activity=False)

    def rating_issued(
            self,
            bounty_id,
            review,
            uid,
            reviewer,
            reviewee,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['RatingIssued'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid='{}-{}'.format(uid, reviewer.id),
            notification_name=notifications['RatingIssued'],
            user=reviewer,
            from_user=reviewee,
            string_data=string_data,
            notification_created=review.created,
            review=review)

    def rating_received(
            self,
            bounty_id,
            review,
            uid,
            reviewer,
            reviewee,
            **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        string_data = notification_templates['RatingReceived'].format(
            bounty_title=bounty.title)
        create_bounty_notification(
            bounty=bounty,
            uid='{}-{}'.format(uid, reviewee.id),
            notification_name=notifications['RatingReceived'],
            user=reviewee,
            from_user=reviewer,
            string_data=string_data,
            notification_created=review.created,
            review=review,
            is_activity=False)

    def profile_updated(self, public_address):
        user = User.objects.get(public_address=public_address)
        string_data = notification_templates['ProfileUpdated'].format(
            public_address=public_address)
        create_profile_updated_notification(
            uid=str(user.id) + str(int(datetime.utcnow().timestamp())) + 'ProfileUpdated',
            notification_name=notifications['ProfileUpdated'],
            user=user,
            from_user=None,
            notification_created=datetime.utcnow(),
            string_data=string_data,
            subject='You Updated Your Profile')
