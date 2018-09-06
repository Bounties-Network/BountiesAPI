import datetime
from decimal import Decimal, Context, ROUND_HALF_UP
import time
import logging
from django.conf import settings

logger = logging.getLogger('django')
max_datetime = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
max_time_stamp = time.mktime(max_datetime.timetuple())
create_token_decimals = Context(prec=6).create_decimal
create_usd_decimals = Context(prec=3).create_decimal


def sqlGenerateOrList(param_name, count, operation):
    index = 0
    sql_string = ''
    while index < count:
        sql_string += '{} {} %s'.format(param_name, operation)
        if index != count - 1:
            sql_string += ' OR '
        index += 1
    return sql_string


def extractInParams(request, equals_param, in_param):
    included_values = []
    equals = request.GET.get(equals_param, None)
    includes_raw = request.GET.get(in_param, None)
    if equals:
        included_values.append(equals)
    if includes_raw:
        includes = includes_raw.split(',')
        included_values = included_values + includes
    if len(included_values) == 0:
        return []
    return included_values


def limitOffsetParams(request):
    offset = request.GET.get('offset', 0)
    try:
        offset = int(offset)
    except ValueError as verr:
        offset = 0
    except Exception as ex:
        offset = 0

    limit = request.GET.get('limit', -1)
    try:
        limit = int(limit)
    except ValueError as verr:
        limit = -1
    except Exception as ex:
        limit = -1

    end_index = -1 if limit == -1 else (offset + limit)
    return offset, end_index


def getDateTimeFromTimestamp(timestamp):
    try:
        integer_stamp = int(timestamp)
    except ValueError:
        logger.error('Incorrect timestamp')
        return max_datetime

    if integer_stamp > max_time_stamp:
        logger.error('Timestamp greater than max')
        return max_datetime
    return datetime.datetime.fromtimestamp(integer_stamp)


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def calculate_token_value(value, decimals):
    return (Decimal(value) / Decimal(pow(10, decimals))
            ).quantize(Decimal(10) ** -decimals)


def base_url_for(platform=None):
    base_url = settings.DEPLOY_URL
    if platform in settings.PLATFORM_MAPPING:
        base_url = settings.PLATFORM_MAPPING[platform]

    return base_url


def bounty_url_for(bounty_id, platform=None):
    url = '{}/bounty/{}/'.format(base_url_for(platform), bounty_id)
    return url


def profile_url_for(public_address, platform=None):
    url = '{}/profile/{}/'.format(base_url_for(platform), public_address)
    return url


def shorten_address(address):
    return '{}...{}'.format(address[:6], address[-4:])


def token_decimals(tokens):
    return create_token_decimals(tokens).quantize(
        Decimal('.00001'), rounding=ROUND_HALF_UP).normalize()


def usd_decimals(tokens):
    return create_usd_decimals(tokens).quantize(
        Decimal('.01'), rounding=ROUND_HALF_UP).normalize()
