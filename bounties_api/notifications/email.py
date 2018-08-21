from django.template.loader import render_to_string
from notifications.constants import notifications

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
	notification_name = ''
	link = ''

	username = ''
	bounty_title = ''
	bounty_categories = []
	usd_amount = 0.0
	token_amount = 0.0
	token = ''
	issuer_address = ''
	user_address = ''
	submission_description = ''
	token_amount_remaining = 0.0
	usd_amount_remaining = 0.0
	remaining_submissions = 0

	notification_to_template = {
		
	}


    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)



    context(self):
    	return {
			'username': self.username,
			'bounty_title': self.bounty_title,
			'bounty_categories': self.bounty_categories,
			'usd_amount': self.usd_amount,
			'token_amount': self.token_amount,
			'token': self.token,
			'issuer_address': self.issuer_address,
			'user_address': self.user_address,
			'submission_description': self.submission_description,
			'token_amount_remaining': self.token_amount_remaining,
			'usd_amount_remaining': self.usd_amount_remaining,
			'remaining_submissions': self.remaining_submissions
    	}




	# def render(self):
	# 	return render_to_string(
	# 		self.template,
	# 		context={

	# 		}
	# 	)





#bouty_categories = []
# <p style="color: #A09CA8; padding: 0.25rem 0.5rem; margin-right: 0.1rem; border: 1px solid lightGrey; border-radius: 25px; display:inline-block; font-size: 0.75rem; font-weight: 400; font-family: 'Inter UI', sans-serif;">Category 1</p>
# <p style="color: #A09CA8; padding: 0.25rem 0.5rem; margin-right: 0.1rem; border: 1px solid lightGrey; border-radius: 25px; display:inline-block; font-size: 0.75rem; font-weight: 400; font-family: 'Inter UI', sans-serif;">Category 2</p>

# bounty profile picture
# default = https://gallery.mailchimp.com/03351ad14a86e9637146ada2a/images/fae20fec-36ab-4594-9753-643c04e0ab9a.png