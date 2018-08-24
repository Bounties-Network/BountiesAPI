from decimal import Context

from django.template.loader import render_to_string

from notifications import constants
from std_bounties.models import Bounty, Category, Review
from bounties.utils import bounty_url_for, profile_url_for

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

	@staticmethod
	def render_categories(categories):
		def render_category(c):
			return render_to_string('category.html', context={ 'category': c })

		return '\n'.join(map(str, map(render_category, categories)))

	def __init__(self, **kwargs):
		if kwargs['notification_name'].__class__ != int:
			raise TypeError('notification_name must be of type int')
		elif kwargs['notification_name'] not in Email.templates:
			raise ValueError(
				'notification_name {} must be a valid notification'.format(
				kwargs['notification_name']))
		if kwargs['bounty'].__class__ != Bounty:
			raise TypeError('bounty must be of type Bounty')

		self.__dict__.update(kwargs)

		user = self.user
		from_user = self.from_user
		issuer = user

		# To fulfiller where issuer is where the notification came from
		if (self.notification_name == constants.FULFILLMENT_ACCEPTED_FULFILLER
			or self.notification_name == constants.RATING_RECEIVED
			or self.notification_name == constants.TRANSFER_RECIPIENT):
			issuer = from_user

		create_decimal = Context(prec=4).create_decimal
		remaining = create_decimal(self.bounty.calculated_balance).normalize()
		token_amount = create_decimal(
			self.bounty.calculated_fulfillmentAmount).normalize()

		self.__dict__.update({
			# TODO: Find the best way to calculate
			# self.usd_amount_remaining = create_decimal(
			# 	bounty.calculated_balance
			# 	* bounty.tokenLockPrice
			# ).normalize()

			'usd_amount': create_decimal(self.bounty.usd_price).normalize(),
			'token_amount': token_amount,
			'token': self.bounty.tokenSymbol,
			'bounty_categories': Email.render_categories(
				self.bounty.data_categories),
			'token_amount_remaining': remaining,
			# TODO: Refactor to remaining submissions on the bounty
			'remaining_submissions': create_decimal(
				remaining / token_amount).normalize(),
			'submission_description': self.bounty.description,
			'issuer_name': issuer and issuer.name,
			'issuer_address': issuer and issuer.public_address,
			'issuer_profile_image': (issuer and issuer.profile_image
					or default_image),
			'issuer_address_link': issuer and profile_url_for(issuer
				.public_address),
			'user_name': user and user.name,
			'user_address': user and user.public_address,
			'user_profile_image': (user and user.profile_image
					or default_image),
			'user_address_link': user and profile_url_for(user
				.public_address),
			'from_user_name': from_user and from_user.name,
			'from_user_address': from_user and from_user.public_address,
			'from_user_profile_image': from_user and from_user.profile_image,
			'from_user_profile_image': (from_user and from_user.profile_image
					or default_image),
			'from_user_address_link': from_user and profile_url_for(from_user
				.public_address),
			'from_user_email': from_user and from_user.email
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
