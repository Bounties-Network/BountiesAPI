# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from django.test import TestCase

# Create your tests here.
from utils.functional_tools import narrower, formatter, merge, pipe
from std_bounties.models import Bounty, Fulfillment

import logging

class BountySubscriberTest(TestCase):
    def setUp(self):
        title = 'Narrowed fields'
        description = 'Tets narrowed function with empty object'
        usd_price = 52.97
        bounty_id = 2222234234
        self.obj = Bounty(title=title, description=description, usd_price=usd_price, bounty_id=bounty_id)
        self.fullfillment = Fulfillment(bounty=self.obj)
        logging.disable(logging.CRITICAL)

    # narrower
    def test_get_attributes_from_bounty_model(self):
        narrowed_fieds = narrower(self.obj, ["title", "usd_price"])

        self.assertEquals(narrowed_fieds['title'], self.obj.title)
        self.assertEquals(narrowed_fieds['usd_price'], self.obj.usd_price)

    def test_get_attributes_with_alias(self):
        narrowed_fieds = narrower(self.obj, [("title", "bounty_name"), ("bounty_id", "id")])

        self.assertEquals(sorted(narrowed_fieds.keys()), ['bounty_name', 'id'])
        self.assertEquals(narrowed_fieds['bounty_name'], self.obj.title)
        self.assertEquals(narrowed_fieds['id'], self.obj.bounty_id)

    def test_get_nested_attributes_using_double_underscore(self):
        narrowed_fieds = narrower(self.fullfillment, [("bounty__title", "title"), "bounty__usd_price"])

        self.assertEquals(sorted(narrowed_fieds.keys()), sorted(['title', 'bounty__usd_price']))
        self.assertEquals(narrowed_fieds['title'], self.obj.title)
        self.assertEquals(narrowed_fieds['bounty__usd_price'], self.obj.usd_price)

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

        self.assertEquals(pipe(0, [p1, p2, p3]), -12)

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
