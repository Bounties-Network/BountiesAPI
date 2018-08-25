from django.db import transaction

from bounties.ses_client import send_email
from bounties.utils import bounty_url_for, profile_url_for

from notifications.models import Notification, DashboardNotification
from notifications.email import Email


def create_bounty_notification(**kwargs):
    bounty = kwargs.get('bounty')
    bounty_url = bounty_url_for(
        bounty.bounty_id, bounty.platform) + kwargs.get('url_query', '')
    kwargs.update({
        'url': bounty_url,
        'platform': bounty.platform
    })
    create_notification(**kwargs)


def create_profile_updated_notification(*args, **kwargs):
    profile_url = profile_url_for(kwargs.get('user').public_address)
    kwargs.update({'url': profile_url})
    create_notification(**kwargs)


@transaction.atomic
def create_notification(**kwargs):
    string_data = kwargs['string_data']
    is_activity = kwargs['is_activity']

    notification, created = Notification.objects.get_or_create(
        uid=str(kwargs['uid']),
        defaults={
            'notification_name': kwargs['notification_name'],
            'user': kwargs['user'],
            'from_user': kwargs['from_user'],
            'notification_created': kwargs['notification_created'],
            'dashboard': True,
            'platform': kwargs['platform'],
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
        data={'link': url, 'bounty_title': kwargs['bounty'].title},
    )

    email_settings = user.settings.emails
    activity_emails = email_settings['activity']

    if is_activity and not activity_emails:
        return

    if (not is_activity and
            notification_name not in user.settings.accepted_email_settings()):
        return

    if notification.email_sent:
        return

    if kwargs['notification_name'] not in Email.templates:
        return  # TODO: Still do regular notification without email

    email = Email(**kwargs)

    # TODO: Remove this - only use while debugging
    email.render_to_file()

    email_html = email.render()

    send_email(user.email, subject, email_txt, email_html)
    notification.email_sent = True
    notification.save()
