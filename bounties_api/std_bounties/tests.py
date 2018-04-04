# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from django.test import TestCase

# Create your tests here.
from std_bounties.client_helpers import narrower, formatter, merge, pipe
from std_bounties.models import Bounty


class BountySubscriberTest(TestCase):
    # narrower
    def test_get_attributes_from_dict(self):
        obj = {'bounty_id': 2222234234, 'bounty_name': 'Narrowed fields'}
        narrowed_fieds = narrower(obj, ["bounty_name", "bounty_id"])

        self.assertEquals(narrowed_fieds.keys(), obj.keys())
        self.assertEquals(narrowed_fieds.values(), obj.values())

    def test_get_attributes_from_bounty_model(self):
        title = 'Narrowed fields'
        description = 'Tets narrowed function with empty object'
        usd_price = 52.97
        bounty = Bounty(title=title, description=description, usd_price=usd_price)
        narrowed_fieds = narrower(bounty, ["title", "usd_price"])

        self.assertEquals(narrowed_fieds['title'], title)
        self.assertEquals(narrowed_fieds['usd_price'], usd_price)

    def test_get_attributes_with_alias_from_dict(self):
        obj = {'bounty_id': 2222234234, 'bounty_name': 'Narrowed fields', 'other': 'Meh!'}
        narrowed_fieds = narrower(obj, [("bounty_name", "title"), ("bounty_id", "id"), 'other'])

        self.assertEquals(narrowed_fieds.keys(), ['title', 'id', 'other'])
        self.assertEquals(narrowed_fieds.values(), obj.values())

    def test_get_nested_attributes_using_double_underscore(self):
        obj = {'bounty_id': 2222234234, 'bounty_name': 'Narrowed fields', 'nested': {
            'key': "nested",
            'value': True
        }}
        narrowed_fieds = narrower(obj, [("bounty_name", "title"), ("nested__key", "id"), "nested__value"])

        self.assertEquals(narrowed_fieds.keys(), ['title', 'id', 'nested__value'])
        self.assertEquals(narrowed_fieds.values(), ['Narrowed fields', 'nested', True])

    # formatter
    def test_format_msg_with_dict(self):
        obj = {'bounty_id': 2222234234, 'bounty_name': 'Narrowed fields', 'nested': True}
        msg = formatter("{bounty_id} has nested values {nested}", obj)
        self.assertEquals(msg, '2222234234 has nested values True')

    # merge
    def test_merge_override_base_keys_when_both_dicts_have_the_same_key(self):
        dict1 = {"color": "Blue", "active": 'False'}
        dict2 = {"place": 'Header', "active": 'True'}

        dict_result = merge(dict1, dict2)

        self.assertEquals(sorted(dict_result.keys()), sorted(['color', 'active', 'place']))
        self.assertEquals(sorted(dict_result.values()), sorted(['Blue', 'Header', 'True']))

    # pipe
    def test_pipe_with_base_value_return_the_same_when_no_functions_are_provided(self):
        self.assertEquals(pipe(5, []), 5)

    def test_pipe_call_each_function_in_the_order_they_are_specified_in_the_array_argument(self):
        def sub(x, y):
            return x - y
        p1 = partial(sub, -1)
        p2 = partial(sub, 3)
        p3 = partial(sub, -8)

        self.assertEquals(pipe(0, [p1, p2, p3]), 6)

    def test_pipe_return_immediately_if_one_function_returns_none(self):
        def sub(x, y):
            return x - y
        side = False
        p1 = partial(sub, -1)

        def p3(value):
            nonlocal side
            side = value

        self.assertEquals(pipe(0, [p1, lambda x: None, p3]), None)
        self.assertEquals(side, False)

    def test_pipe_return_immediately_if_one_exception_is_raised(self):
        def sub(x, y):
            return x - y

        side = False
        p1 = partial(sub, -1)

        def p3(value):
            nonlocal side
            assert False
            side = value

        self.assertEquals(pipe(0, [p1, p3, lambda x: None]), None)
        self.assertEquals(side, False)
