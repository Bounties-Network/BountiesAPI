from functools import partial, update_wrapper
from decimal import Decimal

from bounties import settings
from std_bounties.bounty_client import BountyClient
from std_bounties.client_helpers import bounty_url_for, apply_and_notify, formatted_fulfillment_amount, token_price, format_deadline, usd_price, token_lock_price
from std_bounties.models import Bounty
from utils.functional_tools import merge, narrower, wrapped_partial

from slackclient import SlackClient


bounty_client = BountyClient()
sc = SlackClient(settings.SLACK_TOKEN)


# @with_clients
def bounty_issued(bounty_id, **kwargs):
    msg = "{title}, id: {bounty_id}\n${usd_price}, {total_value} {tokenSymbol} @ ${token_price}\n" \
          "Deadline: {deadline}\n{link} :tada:"
    bounty = Bounty.objects.filter(bounty_id=bounty_id)
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    if not bounty.exists():
        apply_and_notify(bounty_id,
                         event='Bounty Issued',
                         action=bounty_client.issue_bounty,
                         inputs=kwargs,
                         fields=['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals',
                                 'fulfillmentAmount', 'usd_price', 'deadline', 'token'],
                         msg=msg,
                         slack_client=sc,
                         before_formatter=[add_link, formatted_fulfillment_amount, token_price, format_deadline, usd_price]
                         )


# @with_clients
def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}\n${usd_price}, {total_value} {tokenSymbol} @ ${token_price}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Bounty Activated',
                     action=bounty_client.activate_bounty,
                     inputs=kwargs,
                     fields=['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals',
                             'fulfillmentAmount', 'deadline', 'token', 'usd_price'],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link, formatted_fulfillment_amount, token_price, format_deadline, usd_price]
                     )


# @with_clients
def bounty_fulfilled(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Bounty Fulfilled',
                     action=bounty_client.fulfill_bounty,
                     inputs=kwargs,
                     fields=[('bounty__title', 'title'),
                             ('bounty__bounty_id', 'bounty_id'),
                             'fulfillment_id',
                             ('bounty__tokenSymbol', 'tokenSymbol'),
                             ('bounty__tokenDecimals', 'tokenDecimals'),
                             ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                             ('bounty__usd_price', 'usd_price'),
                             ('bounty__deadline', 'deadline')],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def fullfillment_updated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Fulfillment Updated',
                     action=bounty_client.update_fulfillment,
                     inputs=kwargs,
                     fields=[('bounty__title', 'title'),
                             ('bounty__bounty_id', 'bounty_id'),
                             'fulfillment_id'
                             ],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def fulfillment_accepted(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}\n${usd_price}, {total_value} {tokenSymbol} @ ${token_lock_price}\n" \
          "Deadline: {deadline}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Bounty Accepted',
                     action=bounty_client.accept_fulfillment,
                     inputs=kwargs,
                     fields=[('bounty__title', 'title'),
                             ('bounty__bounty_id', 'bounty_id'),
                             'fulfillment_id',
                             ('bounty__tokenSymbol', 'tokenSymbol'),
                             ('bounty__tokenDecimals', 'tokenDecimals'),
                             ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                             ('bounty__usd_price', 'usd_price'),
                             ('bounty__tokenLockPrice', 'token_lock_price'),
                             ('bounty__token', 'token'),
                             ('bounty__deadline', 'deadline')],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link, formatted_fulfillment_amount, token_price, format_deadline, usd_price]
                     )


def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Bounty Killed',
                     action=bounty_client.kill_bounty,
                     inputs=kwargs,
                     fields=['title', 'bounty_id'],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def contribution_added(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)

    msg = "{title}, id: {bounty_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Contribution Added',
                     action=bounty_client.add_contribution,
                     inputs=kwargs,
                     fields=['title',
                             'bounty_id',
                             'tokenDecimals',
                             'balance',
                             'usd_price',
                             'tokenDecimals',
                             'old_balance'
                             ],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def deadline_extended(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    previous_deadline = narrower(bounty, [('deadline', 'previous_deadline')])
    msg = "{title}, id: {bounty_id}\nprevious: {previous_deadline}, new deadline: {deadline}\n{link}"
    mix_previous_deadline = wrapped_partial(merge, source2=previous_deadline)
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Deadline Extended',
                     action=bounty_client.extend_deadline,
                     inputs=kwargs,
                     fields=['title', 'bounty_id', 'deadline'],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[mix_previous_deadline, add_link]
                     )


def bounty_changed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Bounty Changed',
                     action=bounty_client.change_bounty,
                     inputs=kwargs,
                     fields=['title', 'bounty_id'],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def issuer_transfered(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Issuer Transferred',
                     action=bounty_client.transfer_issuer,
                     inputs=kwargs,
                     fields=['title', 'bounty_id'],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    msg = "{title}, id: {bounty_id}\n{link}"
    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

    apply_and_notify(bounty,
                     event='Payout Increased',
                     action=bounty_client.increase_payout,
                     inputs=kwargs,
                     fields=['title',
                             'bounty_id',
                             ],
                     msg=msg,
                     slack_client=sc,
                     before_formatter=[add_link]
                     )