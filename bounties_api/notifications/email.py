from decimal import Context
from textwrap import wrap

from django.template.loader import render_to_string

from notifications import constants
from std_bounties.models import Bounty, Fulfillment
from bounties.utils import (
    bounty_url_for,
    profile_url_for,
    shorten_address,
    calculate_token_value
)
from bounties.settings import ENVIRONMENT

default_image = ('https://gallery.mailchimp.com/03351ad14a86e9637146ada2a'
                 '/images/fae20fec-36ab-4594-9753-643c04e0ab9a.png')


class Email:
    # Supported notification types that have an email template:
    templates = {
        constants.FULFILLMENT_SUBMITTED_ISSUER: 'completedBounty.html',
        constants.FULFILLMENT_ACCEPTED_FULFILLER: 'submissionAccepted.html',
        constants.CONTRIBUTION_ADDED: 'contributionReceived.html',
        constants.ISSUER_TRANSFERRED: 'bountyTransferSent.html',
        constants.TRANSFER_RECIPIENT: 'bountyTransferReceived.html',
        constants.BOUNTY_EXPIRED: 'bountyExpired.html',
        constants.BOUNTY_COMMENT_RECEIVED: 'commentOnBounty.html',
        constants.FULFILLMENT_UPDATED: 'fulfillmentUpdated.html',
        constants.RATING_RECEIVED: 'receivedRating.html',
    }
    max_description_length = 240
    max_title_length = 120

    @staticmethod
    def render_categories(categories):
        def render_category(c):
            return render_to_string('category.html', context={'category': c})

        return '\n'.join(map(str, map(render_category, categories)))

    def __init__(self, **kwargs):
        bounty = kwargs['bounty']
        url = kwargs['url']
        user = kwargs['user']
        from_user = kwargs['from_user']
        notification_name = kwargs['notification_name']
        review = kwargs.get('review')
        issuer = user

        if notification_name.__class__ != int:
            raise TypeError('notification_name must be of type int')
        elif notification_name not in Email.templates:
            raise ValueError(
                'notification_name {} must be a valid notification'.format(
                    notification_name))
        if bounty.__class__ != Bounty:
            raise TypeError('bounty must be of type Bounty')

        # To fulfiller where issuer is where the notification came from
        if (notification_name == constants.FULFILLMENT_ACCEPTED_FULFILLER or
                notification_name == constants.RATING_RECEIVED or
                notification_name == constants.TRANSFER_RECIPIENT):
            issuer = from_user

        create_decimal = Context(prec=4).create_decimal
        remaining = create_decimal(bounty.calculated_balance).normalize()
        token_amount = create_decimal(
            bounty.calculated_fulfillmentAmount).normalize()

        description = bounty.description
        if len(description) > self.max_description_length:
            # Cut off at the closest word after the limit
            description = wrap(
                description, self.max_description_length)[0] + ' ...'

        title = bounty.title
        if len(title) > self.max_title_length:
            # Cut off at the closest word after the limit
            title = wrap(title, self.max_title_length)[0] + ' ...'

        if not url or len(url) == 0:
            url = bounty_url_for(bounty.bounty_id, bounty.platform)

        remaining_submissions = 0

        if notification_name == constants.BOUNTY_EXPIRED:
            remaining_submissions = Fulfillment.objects.filter(
                bounty_id=bounty.id,
                accepted=False,
            ).all().count()

        remaining_usd = ' unknown'
        if bounty.tokenLockPrice:
            remaining_usd = create_decimal(
                remaining * create_decimal(bounty.tokenLockPrice)).normalize()
        elif bounty.token and bounty.token.price_usd:
            remaining_usd = create_decimal(
                remaining * create_decimal(bounty.token.price_usd)).normalize()

        added_amount = 0
        if notification_name == constants.CONTRIBUTION_ADDED:
            inputs = kwargs.get('inputs')
            added_amount = create_decimal(calculate_token_value(
                bounty.tokenDecimals, inputs.fulfillmentAmount))

        self.__dict__.update({
            'bounty': bounty,
            'bounty_title': title,
            'url': url,
            'preferences_link': 'https://{}bounties.network/settings'.format(
                '' if ENVIRONMENT == 'production' else 'staging.'),
            'notification_name': notification_name,
            'usd_amount': create_decimal(bounty.usd_price).normalize(),
            'token_amount': token_amount,
            'token': bounty.tokenSymbol,
            'bounty_categories': Email.render_categories(
                bounty.data_categories),
            'token_amount_remaining': remaining,
            'usd_amount_remaining': remaining_usd,
            'added_amount': added_amount,
            'remaining_submissions': remaining_submissions,
            'submission_description': description,
            'issuer_name': issuer and issuer.name,
            'issuer_address': issuer and shorten_address(
                issuer.public_address),
            'issuer_profile_image': (
                issuer and issuer.profile_image or default_image
            ),
            # TODO: Pass in platform here
            'issuer_address_link': issuer and profile_url_for(
                issuer.public_address),
            'user_name': user and user.name,
            'user_address': user and shorten_address(user.public_address),
            'user_profile_image': (
                user and user.profile_image or default_image
            ),
            # TODO: Pass in platform here
            'user_address_link': user and profile_url_for(user.public_address),
            'from_user_name': from_user and from_user.name,
            'from_user_address': from_user and shorten_address(
                from_user.public_address),
            'from_user_profile_image': (
                from_user and from_user.profile_image or default_image
            ),
            # TODO: Pass in platform here
            'from_user_address_link': from_user and profile_url_for(
                from_user.public_address),  # TODO: Pass in platform here
            'from_user_email': from_user and from_user.email,
            'review': review and review.review,
            'rating': review and '{}/5'.format(review.rating)
        })

    def render(self):
        template = self.templates[self.notification_name]
        return render_to_string(template, context=self.__dict__)

    def render_to_file(self, filename=None):
        if not filename:
            filename = '{}-{}-{}.html'.format(
                self.notification_name,
                self.bounty.bounty_id,
                # Only alphanumeric characters for filename
                ''.join(filter(str.isalnum, self.bounty.title))
            )

        open_file = open(filename, 'w')
        open_file.write(self.render())
        open_file.close()
