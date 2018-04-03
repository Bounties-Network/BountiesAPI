# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from bounties_api.std_bounties.client_helpers import narrower
from bounties_api.std_bounties.models import Bounty


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
        pass

    # formatter
    def test_format_msg_with_dict(self):
        pass

    # merge
    def test_merge_two_dicts(self):
        pass

    def test_merge_override_base_keys_when_both_dicts_have_the_same_key(self):
        pass

    # pipe
    def test_pipe_with_base_value_return_the_same_when_no_functions_are_provided(self):
        pass

    def test_pipe_call_each_function_in_the_order_they_are_specified_in_the_array_argument(self):
        pass

    def test_pipe_return_immediately_if_one_function_returns_none(self):
        pass

    def test_pipe_return_immediately_if_one_exception_is_raised(self):
        pass