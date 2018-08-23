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

	# Values used for email rendering:
	notification_name = -1 # constant from notifications, like BOUNTY_ACTIVATED 
	bounty_title = '' # like "Save the world!"
	# TODO: Set default URL to domain.bounties.network/bounty/bounty_id
	url = '' # link to the bounty itself
	bounty_categories = '' # html with tags/categories for the bounty
	usd_amount = 0.0 # like $42
	token_amount = 0.0 # like 0.42
	token = '' # like ETH
	submission_description = '' # like "Implement a solution to end poverty"
	token_amount_remaining = 0.0 # like 0.42
	usd_amount_remaining = 0.0 # like $42
	remaining_submissions = 0 # the remaining tokens divided by payout cost
	issuer_name = '' # like Ada Lovelace
	issuer_address = '' # like 0xasdfasfdasdf
	issuer_address_link = '' # like https://bounties.network/profile/0x60a...
	issuer_profile_image = default_image # like https://ipfs.infura.io/ipfs/Q..
	user_name = ''
	user_address = ''
	user_address_link = ''
	user_profile_image = default_image
	from_user_name = ''
	from_user_address = ''
	from_user_address_link = ''
	from_user_email = ''
	from_user_profile_image = default_image
	# TODO: Add local/staging/prod link to change preferences in template

	@staticmethod
	def render_categories(categories):

		def render_category(c):
			return render_to_string('category.html', context={ 'category': c })

		return '\n'.join(map(str, map(render_category, categories)))

	@staticmethod
	def extract_users(**kwargs):
		notification_name = kwargs['notification_name']
		user = kwargs['user']
		from_user = kwargs['from_user']
		issuer = user

		# To fulfiller where issuer is where the notification came from
		if (notification_name == constants.FULFILLMENT_ACCEPTED_FULFILLER
			or notification_name == constants.RATING_RECEIVED
			or notification_name == constants.TRANSFER_RECIPIENT):
			issuer = from_user

		return {
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
		}


	def __init__(self, **kwargs):
		notification_name = kwargs['notification_name']
		bounty = kwargs['bounty']

		if notification_name.__class__ != int:
			raise TypeError('notification_name must be of type int')
		if bounty.__class__ != Bounty:
			raise TypeError('bounty must be of type Bounty')
		if notification_name not in Email.templates:
			raise ValueError('notification_name {}'
				' must be a valid notification'.format(notification_name))

		self.__dict__.update(Email.extract_users(**kwargs))

		create_decimal = Context(prec=4).create_decimal

		self.notification_name = notification_name
		self.url = kwargs['url']
		self.bounty_title = kwargs['bounty_title']
		self.usd_amount = create_decimal(bounty.usd_price).normalize()
		self.token_amount = create_decimal(
			bounty.calculated_fulfillmentAmount).normalize()
		self.token = bounty.tokenSymbol
		self.bounty_categories = Email.render_categories(
			bounty.data_categories)
		self.token_amount_remaining = create_decimal(
			bounty.calculated_balance).normalize()

		# TODO: Find the best way to calculate
		# self.usd_amount_remaining = create_decimal(
		# 	bounty.calculated_balance
		# 	* bounty.tokenLockPrice
		# ).normalize()

		# TODO: Remaining possible or remaining actual?
		self.remaining_submissions = create_decimal(
			self.token_amount_remaining / self.token_amount
		).normalize()
		self.submission_description = bounty.description

	def render(self):
		try:
			template = self.templates[self.notification_name]
			return render_to_string(template, context=self.__dict__)
		except KeyError as e:
			raise ValueError('Can\'t render without valid notification_name')

