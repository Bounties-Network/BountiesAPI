from decimal import Decimal
from bounties import settings
from std_bounties.client_helpers import calculate_token_quantity
from bounties.utils import bounty_url_for
from utils.functional_tools import narrower


def notify_slack(sc, channel, event, msg):
    sc.api_call(
        'chat.postMessage',
        channel=channel,
        text='*{}*: {}'.format(
            event,
            msg),
        mrkdwn=True)

    return True


def format_message(fields, msg_string, **kwargs):
    return msg_string.format(**{**fields, **kwargs})


def get_base_bounty_values(bounty):
    base_fields = narrower(bounty, ['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals'])
    base_fields['total_value'] = calculate_token_quantity(bounty.fulfillmentAmount, bounty.tokenDecimals)
    base_fields['usd_price'] = Decimal(bounty.usd_price).quantize(Decimal(10) ** -2)
    base_fields['deadline'] = bounty.deadline.strftime('%m/%d/%Y')
    base_fields['token_price'] = 'Unkown Price' if not bounty.token else Decimal(bounty.token.price_usd).quantize(Decimal(10) ** -2)
    base_fields['token_lock_price'] = 'Unkown Price' if not bounty.tokenLockPrice else Decimal(bounty.tokenLockPrice).quantize(Decimal(10) ** -2)
    base_fields['link'] = bounty_url_for(bounty.bounty_id, bounty.platform)
    return base_fields

