from django.db import transaction

from bounties.ses_client import send_email
from bounties.utils import bounty_url_for, profile_url_for

from notifications.models import Notification, DashboardNotification
from notifications import email_helpers


def create_bounty_notification(**kwargs):
    bounty = kwargs.pop('bounty')
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
def create_notification(
        uid,
        notification_name,
        user,
        from_user,
        notification_created,
        string_data,
        subject,
        bounty_title='',
        is_activity=True,
        string_data_email=None,
        email_button_string='View in App',
        url='',
        platform=''):

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
        data={'link': url, 'bounty_title': bounty_title},
    )

    if is_activity and not activity_emails:
        return

    if not is_activity and notification_name not in
            user.settings.accepted_email_settings():
        return

    if notification.email_sent:
        return
        
    username = 'bounty hunter'
    if user and user.name:
        username = user.name

    email_html = render_to_string(
        'base_notification.html',
        context={
            'link': url,
            'username': username,
            'message_string': string_data_email or string_data,
            'button_text': email_button_string})
    email_txt = 'Hello {}! \n {}'.format(
        username, string_data_email or string_data, )
    email_settings = user.settings.emails
    activity_emails = email_settings['activity']

    send_email(user.email, subject, email_txt, email_html)
    notification.email_sent = True
    notification.save()
