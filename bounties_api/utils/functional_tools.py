from rest_framework import serializers

import collections
import logging
from functools import partial, update_wrapper

logger = logging.getLogger('django')


def pluck(dictionary, fields):
    """Extract fields from dict and return a dict"""
    return {key: dictionary.get(key, '') for key in fields}

def narrower(obj, fields):
    """Extract fields from obj and return a dict"""
    narrowed_fields = {}
    for field in fields:
        attr = field
        key = field
        current_obj = obj

        if type(field) is tuple:
            attr = field[0]
            key = field[1]

        try:
            for nested_attr in attr.split('__'):
                value = getattr(current_obj, nested_attr)
                current_obj = value

            narrowed_fields[key] = value
        except AttributeError as e:
            logger.error(str(e), exc_info=True)
            return

    return narrowed_fields


def formatter(msg, values):
    """Functional form of format on strings"""
    return msg.format(**values)


def merge(source1, source2):
    """Merge two dicts, source2 could override existing keys based on source1"""
    return {**source1, **source2}


def wrapped_partial(func, *args, **kwargs):
    """Mimic tha partial applied function to get name and docs associated to the original function"""
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


def flatten(l):
    """Flat irregular list
    Credits to: https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists"""
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def pipe(initial_value, functions):
    """Call function with the result of the precious functions.
    At the first function call, initial value is passed as argument"""
    current_result = initial_value
    for f in functions:
        try:
            current_result = f(current_result)
            # logger.warning("--- {} -> {}".format(f.__name__, current_result))

            if current_result is None:
                logger.warning("{} returns None with the given arg: {}".format(f.__name__, current_result))
                return
        except serializers.ValidationError:
            raise
        except Exception as e:
            logger.error(
                "{} - {} raised exception with the given arg: {}, ".format(str(e),
                                                                           f.__name__, current_result),
                exc_info=True)
            return

    return current_result
