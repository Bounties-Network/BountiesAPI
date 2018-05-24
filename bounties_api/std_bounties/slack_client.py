from bounties import settings
from utils.functional_tools import wrapped_partial, pipe, pluck
from std_bounties.slack_templates import *
from std_bounties.slack_client_helpers import notify_slack, get_base_bounty_values, format_message
from slackclient import SlackClient


sc = SlackClient(settings.SLACK_TOKEN)
channel = settings.NOTIFICATIONS_SLACK_CHANNEL

class SlackMessageClient:

    def __init__(self):
        pass

    def bounty_issued(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'usd_price', 'total_value', 'tokenSymbol', 'token_price',
            'deadline', 'link', 'total_value'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_ISSUED_SLACK_STR)])
        notify_slack(sc, channel, 'Bounty Issued', message)


    def bounty_issued_and_activated(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'usd_price', 'total_value', 'tokenSymbol', 'token_price',
            'deadline', 'link', 'total_value'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_ISSUED_SLACK_STR)])
        notify_slack(sc, channel, 'Bounty Issued and Activated', message)


    def bounty_activated(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'usd_price', 'total_value', 'tokenSymbol', 'token_price', 'link'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_ACTIVATED_SLACK_STR)])
        notify_slack(sc, channel, 'Bounty Activated', message)


    def bounty_fulfilled(self, bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_FULFILLED_SLACK_STR, fulfillment_id=fulfillment_id)])
        notify_slack(sc, channel, 'Bounty Fulfilled', message)


    def fulfillment_updated(self, bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=FULFILLED_UPDATED_SLACK_STR, fulfillment_id=fulfillment_id)])
        notify_slack(sc, channel, 'Fulfillment Updated', message)


    def fulfillment_accepted(self, bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'usd_price', 'total_value', 'tokenSymbol', 'token_price',
            'deadline', 'link', 'token_lock_price'
        ]), wrapped_partial(format_message, msg_string=FULFILLMENT_ACCEPTED_SLACK_STR, fulfillment_id=fulfillment_id)])
        notify_slack(sc, channel, 'Fulfillment Accepted', message)


    def bounty_killed(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_KILLED_SLACK_STR)])
        notify_slack(sc, channel, 'Bounty Killed', message)


    def contribution_added(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=CONTRIBUTION_ADDED_SLACK_STR)])
        notify_slack(sc, channel, 'Contribution Added', message)


    def deadline_extended(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'deadline', 'link'
        ]), wrapped_partial(format_message, msg_string=DEADLINE_EXTENDED_SLACK_STR)])
        notify_slack(sc, channel, 'Deadline Extended', message)


    def bounty_changed(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=BOUNTY_CHANGED_SLACK_STR)])
        notify_slack(sc, channel, 'Bounty Changed', message)


    def issuer_transferred(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=ISSUER_TRANSFERRED_SLACK_STR)])
        notify_slack(sc, channel, 'Issuer Transferred', message)


    def payout_increased(self, bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, fields=[
            'title', 'bounty_id', 'link'
        ]), wrapped_partial(format_message, msg_string=PAYOUT_INCREASED_SLACK_STR)])
        notify_slack(sc, channel, 'Payout Increased', message)
