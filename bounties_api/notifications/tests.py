import unittest

from notifications.email import Email

def load_template(template):
	with fopen('./test_templates/{}'.format(template)):
		return ...


class TestComment(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_issuer_comment_notification(self):
    	issuer_comment_event = {
    		...
    	}

        expected = load_template('test_issuer_comment_notification.html')

        email = Email(issuer_comment_event)
        result = email.render()

        self.assertEqual(result, expected)


