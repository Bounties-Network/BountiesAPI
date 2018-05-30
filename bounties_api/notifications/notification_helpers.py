from django.template.loader import render_to_string
from notifications.models import Notification, DashboardNotification
from bounties.ses_client import send_email
from bounties.utils import bounty_url_for


def create_notification(bounty, notification_name, user, notification_created, string_data, subject, is_activity=True, email=False):
    bounty_url = bounty_url_for(bounty.bounty_id, bounty.platform)
    notification = Notification.objects.create(
        notification_name=notification_name,
        user=user,
        notification_created=notification_created,
        email=email,
        dashboard=True
    )
    DashboardNotification.objects.create(
        notification=notification,
        string_data=string_data,
        is_activity=is_activity,
        data={'link': bounty_url},
    )
    username = bounty.user.name or 'bounty hunter'
    email_html = render_to_string('base_notification.html', context={'link': bounty_url, 'username': username, 'message_string': string_data})
    email_txt = 'Hello {}! \n {} \n View in app: {}'.format(username, string_data, bounty_url)
    if bounty.platform != 'gitcoin':
        send_email(bounty.user.email, subject, email_txt, email_html)
