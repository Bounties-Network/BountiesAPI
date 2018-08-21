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
	message_string = ''
	button_text = ''

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)



	def render(self):
		return render_to_string(
			self.template,
			context={

			}
		)



#bouty_categories = []
# <p style="color: #A09CA8; padding: 0.25rem 0.5rem; margin-right: 0.1rem; border: 1px solid lightGrey; border-radius: 25px; display:inline-block; font-size: 0.75rem; font-weight: 400; font-family: 'Inter UI', sans-serif;">Category 1</p>
# <p style="color: #A09CA8; padding: 0.25rem 0.5rem; margin-right: 0.1rem; border: 1px solid lightGrey; border-radius: 25px; display:inline-block; font-size: 0.75rem; font-weight: 400; font-family: 'Inter UI', sans-serif;">Category 2</p>