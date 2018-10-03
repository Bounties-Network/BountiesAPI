from textwrap import wrap
from decimal import Decimal

from django.template.loader import render_to_string
from django.db.models import Avg

from notifications import constants
from std_bounties.models import Bounty, Fulfillment
from bounties.utils import (
    bounty_url_for,
    profile_url_for,
    shorten_address,
    calculate_token_value,
    token_decimals,
    usd_decimals
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
        constants.CONTRIBUTION_RECEIVED: 'contributionReceived.html',
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

    @staticmethod
    def rating_color(rating):
        if rating >= 4:
            return '#6FC78D'  # 'brand-green'
        elif rating >= 3:
            return '#FBAA31'  # 'brand-orange'
        else:
            return '#D14545'  # 'brand-red'

    def __init__(self, **kwargs):
        bounty = kwargs['bounty']
        url = kwargs['url']
        user = kwargs['user']
        from_user = kwargs['from_user']
        notification_name = kwargs['notification_name']
        review = kwargs.get('review')
        comment = kwargs.get('comment')
        description = kwargs.get('fulfillment_description', '')
        preview_text = kwargs.get('string_data', '')

        if notification_name.__class__ != int:
            raise TypeError('notification_name must be of type int')
        elif notification_name not in Email.templates:
            raise ValueError(
                'notification_name {} must be a valid notification'.format(
                    notification_name))
        if bounty.__class__ != Bounty:
            raise TypeError('bounty must be of type Bounty')

        issuer = bounty.user

        remaining = token_decimals(bounty.calculated_balance)
        token_amount = token_decimals(
            bounty.calculated_fulfillmentAmount)

        if len(description) > self.max_description_length:
            # Cut off at the closest word after the limit
            description = wrap(
                description,
                self.max_description_length
            )[0] + ' ...'

        title = bounty.title
        if len(title) > self.max_title_length:
            # Cut off at the closest word after the limit
            title = wrap(title, self.max_title_length)[0] + ' ...'

        if not url or len(url) == 0:
            url = bounty_url_for(bounty.bounty_id, bounty.platform)

        remaining_submissions = 0

        if (notification_name == constants.BOUNTY_EXPIRED or
                notification_name == constants.CONTRIBUTION_RECEIVED or
                notification_name == constants.CONTRIBUTION_ADDED):
            remaining_submissions = Fulfillment.objects.filter(
                bounty_id=bounty.id,
                accepted=False,
            ).all().count()

        remaining_usd = ' unknown'
        if bounty.tokenLockPrice:
            remaining_usd = usd_decimals(
                remaining * usd_decimals(bounty.tokenLockPrice))
        elif bounty.token and bounty.token.price_usd:
            remaining_usd = usd_decimals(
                remaining * usd_decimals(bounty.token.price_usd))

        added_amount = 0
        if (notification_name == constants.CONTRIBUTION_RECEIVED or
                notification_name == constants.CONTRIBUTION_ADDED):
            inputs = kwargs['inputs']
            added_amount = token_decimals(calculate_token_value(
                int(Decimal(inputs['value'])), bounty.tokenDecimals))

        rating_url = url
        if notification_name == constants.FULFILLMENT_ACCEPTED_FULFILLER:
            rating_url = '{}?fulfillment_id={}&rating=true'.format(
                url, kwargs['fulfillment_id'])

        ratings = None
        if notification_name == constants.RATING_RECEIVED:
            user_reviewees = user.reviewees.filter(platform=bounty.platform)

            if user.public_address == issuer.public_address:
                # Rating for the issuer from the fulfiller
                ratings = user_reviewees.filter(
                    issuer_review__isnull=False)
            else:
                # Rating for the fulfiller from the issuer
                ratings = user_reviewees.filter(
                    fulfillment_review__isnull=False)

        rating_count = ratings and ratings.count() or 0
        average_rating = ratings and ratings.aggregate(
            Avg('rating')).get('rating__avg') or 0

        self.__dict__.update({
            'bounty': bounty,
            'bounty_title': title,
            'url': url,
            'preferences_link': 'https://{}bounties.network/settings'.format(
                '' if ENVIRONMENT == 'production' else 'staging.'),
            'notification_name': notification_name,
            'usd_amount': usd_decimals(bounty.usd_price),
            'token_amount': token_amount,
            'token': bounty.tokenSymbol,
            'bounty_categories': Email.render_categories(
                bounty.data_categories),
            'token_amount_remaining': remaining,
            'usd_amount_remaining': remaining_usd,
            'added_amount': added_amount,
            'remaining_submissions': remaining_submissions,
            'fulfillment_description': description,
            'issuer_name': issuer and issuer.name,
            'issuer_address': issuer and shorten_address(
                issuer.public_address),
            'issuer_profile_image': (
                issuer and issuer.small_profile_image_url or default_image
            ),
            'issuer_address_link': issuer and profile_url_for(
                issuer.public_address, bounty.platform),
            'user_name': user and user.name,
            'user_address': user and shorten_address(user.public_address),
            'user_profile_image': (
                user and user.small_profile_image_url or default_image
            ),
            'user_address_link': user and profile_url_for(
                user.public_address, bounty.platform),
            'from_user_name': from_user and from_user.name,
            'from_user_address': from_user and shorten_address(
                from_user.public_address),
            'from_user_profile_image': (
                from_user and from_user.small_profile_image_url or default_image
            ),
            'from_user_address_link': from_user and profile_url_for(
                from_user.public_address, bounty.platform),
            'from_user_email': from_user and from_user.email,
            'review': review and review.review,
            'rating': review and '{}/5'.format(review.rating),
            'rating_color': review and Email.rating_color(review.rating),
            'comment': comment and comment.text,
            'MC_PREVIEW_TEXT': preview_text,
            'rating_url': rating_url,
            'average_rating': usd_decimals(average_rating),
            'rating_count': rating_count
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
