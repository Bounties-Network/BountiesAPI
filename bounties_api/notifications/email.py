from django.template.loader import render_to_string

from notifications import constants
from std_bounties.models import Bounty, Category, Review

# string_data = notification_templates['BountyIssued'].format(
#     bounty_title=bounty.title)

# create_bounty_notification(
#     bounty=bounty,
#     uid=uid,
#     notification_name=notifications['BountyIssued'],
#     user=bounty.user,
#     from_user=None,
#     string_data=string_data,
#     bounty_title=bounty.title,
#     subject='New bounty issued')

class Email:
	default_picture = 'https://gallery.mailchimp.com/03351ad14a86e9637146ada2a/images/fae20fec-36ab-4594-9753-643c04e0ab9a.png'

	# Supported notification types that have an email template:
	templates = {
		# FULFILLMENT_SUBMITTED: '',
		constants.FULFILLMENT_SUBMITTED_ISSUER: 'completedBounty.html',
		# BOUNTY_ACTIVATED: '',
		# FULFILLMENT_ACCEPTED: '',
		constants.FULFILLMENT_ACCEPTED_FULFILLER: 'submissionAccepted.html',
		constants.BOUNTY_EXPIRED: 'bountyExpired.html',
		# BOUNTY_ISSUED: '',
		# BOUNTY_KILLED: '',
		constants.CONTRIBUTION_ADDED: 'contributionReceived.html',
		# DEADLINE_EXTENDED: '',
		# BOUNTY_CHANGED: '',
		constants.ISSUER_TRANSFERRED: 'bountyTransferSent.html',
		constants.TRANSFER_RECIPIENT: 'bountyTransferReceived.html',
		# PAYOUT_INCREASED: '',
		constants.BOUNTY_EXPIRED: 'bountyExpired.html',
		constants.BOUNTY_COMMENT_RECEIVED: 'commentOnBounty.html',
		# BOUNTY_ISSUED_ACTIVATED: '',
		constants.FULFILLMENT_UPDATED: 'fulfillmentUpdated.html',
		# FULFILLMENT_UPDATED_ISSUER: '',
		# RATING_ISSUED: '',
		constants.RATING_RECEIVED: 'receivedRating.html',
		# PROFILE_UPDATED: '',
		# BOUNTY_COMMENT: '',
	}

	# Values used for email rendering:
	notification_name = 0
	link = ''
	username = ''
	bounty_title = ''
	bounty_categories = []
	usd_amount = 0.0
	token_amount = 0.0
	token = ''
	issuer_address = ''
	issuer_address_link = ''
	user_address = ''
	user_address_link = ''
	submission_description = ''
	token_amount_remaining = 0.0
	usd_amount_remaining = 0.0
	remaining_submissions = 0
	bounty_profile_picture = default_picture
	user_profile_picture = default_picture


	def __init__(self, notification_name, bounty):
		if notification_name.__class__ != int:
			raise TypeError('notification_name must be of type int')
		if bounty.__class__ != Bounty:
			raise TypeError('bounty must be of type Bounty')
		if notification_name not in constants.notifications:
			raise ValueError('notification_name must be a valid notification')

		self.link = bounty.url
		self.username = bounty.username
		self.bounty_title = bounty.bounty_title
		self.bounty_categories = bounty.categories
		self.usd_amount = bounty.usd_price
		self.token_amount = bounty.token
		self.token = bounty.calculated_fulfillmentAmount.strip('0')
		# self.issuer_address = bounty.''
		# self.issuer_address_link = bounty.''
		# self.user_address = bounty.''
		# self.user_address_link = bounty.''
		# self.submission_description = bounty.''
		# self.token_amount_remaining = bounty.0.0
		# self.usd_amount_remaining = bounty.0.0
		# self.remaining_submissions = bounty.0
		# self.bounty_profile_picture = bounty.default_picture
		# self.user_profile_picture = bounty.default_picture

	def context(self):
		return {
			'username': self.username,
			'bounty_title': self.bounty_title,
			'bounty_categories': self.render_categories(),
			'usd_amount': self.usd_amount,
			'token_amount': self.token_amount,
			'token': self.token,
			'issuer_address': self.issuer_address,
			'user_address': self.user_address,
			'submission_description': self.submission_description,
			'token_amount_remaining': self.token_amount_remaining,
			'usd_amount_remaining': self.usd_amount_remaining,
			'remaining_submissions': self.remaining_submissions,
			'bounty_profile_picture': self.bounty_profile_picture,
			'user_profile_picture': self.user_profile_picture
		}

	def render(self):
		try:
			template = self.templates[self.notification_name]

			return render_to_string(template, context=self.context())
		except KeyError as e:
			raise ValueError('Can\'t render without valid notification_name')

	def render_categories(self):
		def render_category(c):
			return render_to_string('category.html', context={ 'category': c })

		return map(render_category, self.bounty_categories)
