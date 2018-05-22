from bounties import settings
from utils.functional_tools import wrapped_partial, pipe

from slackclient import SlackClient


sc = SlackClient(settings.SLACK_TOKEN)
channel = settings.NOTIFICATIONS_SLACK_CHANNEL

class SlackMessageClient:

    def __init__(self):
        pass

    def bounty_issued(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'usd_price', 'token_value', 'tokenSymbol', 'token_price',
            'deadline', 'link'
        ])], wrapped_partial(format_message, BOUNTY_ISSUED_SLACK_STR))
        notify_slack(sc, channel, 'Bounty Issued', message)


    def bounty_activated(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'usd_price', 'token_value', 'tokenSymbol', 'token_price', 'link'
        ])], wrapped_partial(format_message,BOUNTY_ACTIVATED_SLACK_STR))
        notify_slack(sc, channel, 'Bounty Activated', message)


    def bounty_fulfilled(bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, BOUNTY_FULFILLED_SLACK_STR, fulfillment_id=fulfillment_id))
        notify_slack(sc, channel, 'Bounty Fulfilled', message)


    def fulfillment_updated(bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, FULFILLED_UPDATED_SLACK_STR, fulfillment_id=fulfillment_id))
        notify_slack(sc, channel, 'Fulfillment Updated', message)


    def fulfillment_accepted(bounty, fulfillment_id):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'usd_price', 'token_value', 'tokenSymbol', 'token_price',
            'deadline', 'link'
        ])], wrapped_partial(format_message,FULFILLMENT_ACCEPTED_SLACK_STR, fulfillment_id=fulfillment_id))
        notify_slack(sc, channel, 'Fulfillment Accepted', message)


    def bounty_killed(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, BOUNTY_KILLED_SLACK_STR))
        notify_slack(sc, channel, 'Bounty Killed', message)


    def contribution_added(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, CONTRIBUTION_ADDED_SLACK_STR))
        notify_slack(sc, channel, 'Contribution Added', message)


    def deadline_extended(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'deadline', 'link'
        ])], wrapped_partial(format_message, DEADLINE_EXTENDED_SLACK_STR))
        notify_slack(sc, channel, 'Deadline Extended', message)


    def bounty_changed(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, BOUNTY_CHANGED_SLACK_STR))
        notify_slack(sc, channel, 'Bounty Changed', message)


    def issuer_transferred(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, ISSUER_TRANSFERRED_SLACK_STR))
        notify_slack(sc, channel, 'Issuer Transferred', message)


    def payout_increased(bounty):
        message = pipe(bounty, [get_base_bounty_values, wrapped_partial(pluck, [
            'title', 'bounty_id', 'link'
        ])], wrapped_partial(format_message, PAYOUT_INCREASED_SLACK_STR))
        notify_slack(sc, channel, 'Payout Increased', message)
