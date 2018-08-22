from django.db import transaction

from bounties.ses_client import send_email
from bounties.utils import bounty_url_for, profile_url_for

from notifications.models import Notification, DashboardNotification
from notifications.email import Email


def create_bounty_notification(**kwargs):
    bounty = kwargs.get('bounty')
    bounty_url = bounty_url_for(
        bounty.bounty_id, bounty.platform) + kwargs.get('url_query', '')


    print('-------------------------')
    print()
    print()
    print('notifiation_helpers.py create_bounty_notification')
    print(bounty_url)
    print()
    print()
    print('-------------------------')
    print('-------------------------')

    kwargs.update({
        'url': bounty_url,
        'platform': bounty.platform
    })
    create_notification(**kwargs)


def create_profile_updated_notification(*args, **kwargs):
    profile_url = profile_url_for(kwargs.get('user').public_address)

    print('-------------------------')
    print()
    print()
    print('notifiation_helpers.py create_profile_updated_notification')
    print(profile_url)
    print()
    print()
    print('-------------------------')
    print('-------------------------')

    kwargs.update({'url': profile_url})
    create_notification(**kwargs)


# @transaction.atomic
# def create_notification(
#         bounty,
#         uid,
#         notification_name,
#         user,
#         from_user,
#         notification_created,
#         string_data,
#         subject,
#         bounty_title='',
#         is_activity=True,
#         string_data_email=None,
#         url='',
#         platform=''):
@transaction.atomic
def create_notification(**kwargs):

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

    # DashboardNotification.objects.create(
    #     notification=notification,
    #     string_data=string_data,
    #     is_activity=is_activity,
    #     data={'link': url, 'bounty_title': bounty_title},
    # )

    # email_settings = user.settings.emails
    # activity_emails = email_settings['activity']

    # if is_activity and not activity_emails:
    #     return

    # if (not is_activity and
    #     notification_name not in user.settings.accepted_email_settings()):
    #     return

    # if notification.email_sent:
    #     return
        
    # username = 'bounty hunter'
    # if user and user.name:
    #     username = user.name

    if kwargs['notification_name'] not in Email.templates:
        return # TODO: Still do regular notification without email?


    email = Email(**kwargs)

    email_html = email.render()

    # Open a file
    nn = kwargs['notification_name']
    bid = kwargs['bounty_id']
    fo = open('{}-{}.html'.format(nn, bid), 'wb')
    fo.write(email_html)

    # Close opend file
    fo.close()


    # email_txt = 'Hello {}! \n {}'.format(
    #     username, string_data_email or string_data, )

    # send_email(user.email, subject, email_txt, email_html)
    # notification.email_sent = True
    # notification.save()
