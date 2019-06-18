from django.db import transaction

from bounties import settings
from bounties.ses_client import send_email
from bounties.utils import bounty_url_for, profile_url_for

from notifications.models import Notification, DashboardNotification
from notifications.email import Email


def create_bounty_notification(**kwargs):
    bounty = kwargs.get('bounty')
    bounty_url = bounty_url_for(bounty.id, bounty.platform) + kwargs.get('url_query', '')
    kwargs.update({
        'url': bounty_url,
        'platform': bounty.platform
    })
    create_notification(**kwargs)


def create_profile_updated_notification(*args, **kwargs):
    profile_url = profile_url_for(kwargs.get('user').public_address)
    kwargs.update({'url': profile_url})
    create_notification(**kwargs)


def create_rating_notification(**kwargs):
    bounty = kwargs.get('bounty')
    issuer = bounty.user
    review = kwargs.get('review')
    user = review.reviewee

    reviewee = 'fulfiller'
    if user.public_address == issuer.public_address:
        # Rating for the issuer from the fulfiller
        reviewee = 'issuer'

    profile_url = profile_url_for(user.public_address)
    kwargs.update({
        'url': profile_url + '?reviews=true&{}=true'.format(reviewee),
        'platform': bounty.platform
    })
    create_notification(**kwargs)


@transaction.atomic
def create_notification(**kwargs):
    uid = kwargs['uid']
    notification_name = kwargs['notification_name']
    string_data = kwargs['string_data']
    user = kwargs['user']
    from_user = kwargs['from_user']
    notification_created = kwargs['notification_created']
    bounty = kwargs.get('bounty')
    subject = kwargs['subject']
    platform = kwargs.get('platform', '')
    is_activity = kwargs.get('is_activity', True)
    url = kwargs.get('url', '')

    notification, created = Notification.objects.get_or_create(
        uid=str(uid),
        defaults={
            'notification_name': notification_name,
            'user': user,
            'from_user': from_user,
            'notification_created': notification_created,
            'dashboard': True,
            'platform': platform,
        },
    )

    # this function is atomic, so this is a good way to be sure
    # we never notify more than once
    if not created:
        return

    DashboardNotification.objects.create(
        notification=notification,
        string_data=string_data,
        is_activity=is_activity,
        data={
            'link': url,
            'bounty_title': bounty and bounty.title or kwargs.get('subject')
        },
    )

    # from here on out, all we care about is email
    if not user.email:
        return

    email_settings = user.settings.emails
    activity_emails = email_settings['activity']

    print('is activity')
    print(is_activity)
    if is_activity and not activity_emails:
        return

    print('is allowed email')
    if (not is_activity and notification_name not in user.settings.accepted_email_settings()):
        return

    print('about to send email')

    if platform not in settings.PLATFORM_MAPPING:
        return

    print('not included platform')

    if notification.email_sent:
        return

    print('email already sent')

    if notification_name not in Email.templates:
        return

    print('1')
    email = Email(**kwargs)
    print('2')
    email_html = email.render()
    print('3')
    send_email(user.email, subject, email_html)
    print('email sent')
    notification.email_sent = True
    notification.save()
