from notifications.models import Notification, DashboardNotification
from bounties.utils import profile_url_for
from std_bounties.models import Bounty, Fulfillment, Review


def fix_it_all():
    for notification in Notification.objects.filter(notification_name=19):
        print()
        print('looping with notification {}'.format(notification.__dict__))
        print()
        dn = DashboardNotification.objects.get(id=notification.id)
        print()
        print('looping with dn {}'.format(dn.__dict__))
        print()
        title = dn.data['bounty_title']
        bounties = Bounty.objects.filter(title=title)
        if len(bounties) > 1:
            print()
            print()
            print('GOT MULTIPLE BOUNTIES FOR TITLE: {}'.format(title))
            print()
            print()
            continue

        bounty = bounties[0]
        print()
        print('looping with bounty {}'.format(bounty.__dict__))
        print()

        fulfillments = Fulfillment.objects.filter(bounty_id=bounty.bounty_id)
        for fulfillment in fulfillments:
            print()
            print('looping with fulfillment {}'.format(fulfillment.__dict__))
            print()

            if fulfillment.issuer_review_id:
                fix_issuer(fulfillment, dn)


def fix_issuer(fulfillment, dn):
    review = Review.objects.get(id=fulfillment.issuer_review_id)
    issuer = Bounty.objects.get(id=fulfillment.bounty_id).issuer
    update_dash_notification(issuer, review.reviewee, dn)


# WARNING - This will modify notifications in the database
# Use with caution and test on your local database first!

def update_dash_notification(issuer_address, user, dash):
    reviewee = 'fulfiller'

    print()
    print('running update_dash_notification with {} {} {}'.format(
        issuer_address, user, dash))
    print()

    if user.public_address == issuer_address:
        # Rating for the issuer from the fulfiller
        reviewee = 'issuer'

    profile_url = profile_url_for(user.public_address)
    url = profile_url + '?reviews=true&{}=true'.format(reviewee)
    print('changing dash notification from:')
    print(dash.__dict__)
    print()
    dash.data['link'] = url
    print('to:')
    print(dash.__dict__)
    print()

    print('NOT UPDATING (uncomment here to actually update)')
    # dash.save()
