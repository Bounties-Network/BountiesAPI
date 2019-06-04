import unittest

from datetime import datetime
from std_bounties.bounty_client import BountyClient
from std_bounties.models import Bounty, Fulfillment
from std_bounties.constants import ACTIVE_STAGE, DRAFT_STAGE, COMPLETED_STAGE, DEAD_STAGE


class TestBountyClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = BountyClient()

    def test_issue_bounty(self):
        bounty_id = 25
        issuer = '0x4242424242424242424242424242424242424242'
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL',
            'paysTokens': False,
            'tokenContract': '0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359',
            'fulfillmentAmount': 1,
            'issuer': issuer,
            'deadline': '1550529106',
        }
        issue_timestamp = '1517536922'
        issue_datetime = datetime.fromtimestamp(int(issue_timestamp))
        bounty = self.client.issue_bounty(
            bounty_id=bounty_id,
            inputs=inputs,
            event_timestamp=issue_timestamp)
        self.assertEqual(bounty.id, bounty_id)
        self.assertEqual(bounty.bounty_id, bounty_id)
        self.assertEqual(bounty.bounty_created, issue_datetime)
        self.assertEqual(bounty.bountyStage, DRAFT_STAGE)
        self.assertEqual(bounty.issuer, issuer)

    def test_activate_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_activate = Bounty(
            id=1,
            bounty_id=1,
            fulfillmentAmount=1,
            usd_price=1,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=DRAFT_STAGE)
        bounty_to_activate.save()
        bounty_to_activate_id = bounty_to_activate.id
        # Activate bounty
        activation_timestamp = '1517536922'
        bounty_to_activate = Bounty.objects.get(pk=bounty_to_activate_id)

        result = self.client.activate_bounty(
            bounty=bounty_to_activate,
            inputs={},
            event_timestamp=activation_timestamp)

        self.assertEqual(result.bountyStage, ACTIVE_STAGE)

        activated_bounty_from_db = Bounty.objects.get(
            pk=bounty_to_activate_id)
        self.assertEqual(result, activated_bounty_from_db)

    def test_fulfill_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_fulfill = Bounty(
            id=2,
            bounty_id=2,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_fulfill.save()
        bounty_to_fulfill_id = bounty_to_fulfill.id
        # Fulfill bounty
        bounty_to_fulfill = Bounty.objects.get(pk=bounty_to_fulfill_id)
        fulfillment_timestamp = '1517536922'
        fulfillment_datetime = datetime.fromtimestamp(int(fulfillment_timestamp))
        fulfillment_id = 10
        issuer = '0x4242424242424242424242424242424242424242'
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL'
        }
        fulfillment = self.client.fulfill_bounty(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_id,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp,
            transaction_issuer=issuer)

        self.assertEqual(fulfillment.fulfillment_id, fulfillment_id)
        self.assertEqual(fulfillment.bounty.id, bounty_to_fulfill_id)
        self.assertEqual(fulfillment.accepted, False)
        self.assertEqual(fulfillment.fulfiller, issuer)
        self.assertEqual(fulfillment.fulfillment_created, fulfillment_datetime)

        # Try fulfill with duplicate id
        fulfillment = self.client.fulfill_bounty(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_id,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp,
            transaction_issuer=issuer)
        self.assertIsNone(fulfillment)

    def test_accept_fulfillment(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_fulfill = Bounty(
            id=3,
            bounty_id=3,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_fulfill.save()
        bounty_to_fulfill_id = bounty_to_fulfill.id
        # Create fulfillment
        fulfillment_to_accept = Fulfillment(
            fulfillment_id=1,
            fulfiller='0x4242424242424242424242424242424242424242',
            bounty=bounty_to_fulfill,
            accepted=True,
            created=created)
        fulfillment_to_accept.save()
        fulfillment_to_accept_id = fulfillment_to_accept.id
        # Accept fulfillment
        bounty_to_fulfill = Bounty.objects.get(pk=bounty_to_fulfill_id)
        fulfillment_timestamp = '1517536922'
        fulfillment_datetime = datetime.fromtimestamp(int(fulfillment_timestamp))
        fulfillment_to_accept = Fulfillment.objects.get(pk=fulfillment_to_accept_id)
        fulfillment = self.client.accept_fulfillment(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_to_accept.fulfillment_id,
            event_timestamp=fulfillment_timestamp)
        self.assertEqual(fulfillment.bounty.bountyStage, COMPLETED_STAGE)
        self.assertEqual(fulfillment.accepted, True)
        self.assertEqual(fulfillment.accepted_date, fulfillment_datetime)
        self.assertEqual(bounty_to_fulfill.balance, 0)

    def test_kill_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_kill = Bounty(
            id=4,
            bounty_id=4,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=ACTIVE_STAGE)
        bounty_to_kill.save()
        bounty_to_kill_id = bounty_to_kill.id
        # Kill bounty
        bounty_to_kill = Bounty.objects.get(pk=bounty_to_kill_id)
        fulfillment_timestamp = '1517536922'
        bounty = self.client.kill_bounty(
            bounty=bounty_to_kill,
            event_timestamp=fulfillment_timestamp)
        self.assertEqual(bounty.bountyStage, DEAD_STAGE)

    def test_add_contribution(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_top_up = Bounty(
            id=5,
            bounty_id=5,
            balance=0,
            fulfillmentAmount=10,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=COMPLETED_STAGE)
        bounty_to_top_up.save()
        bounty_to_top_up_id = bounty_to_top_up.id
        # Top up bounty with amount that is not enough to make it active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 2
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, COMPLETED_STAGE)
        self.assertEqual(bounty.balance, new_balance)
        # Top up bounty with amount enough to make it active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 10
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, ACTIVE_STAGE)
        self.assertEqual(bounty.balance, new_balance)
        # Top up bounty that is already active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 10
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, ACTIVE_STAGE)
        self.assertEqual(bounty.balance, new_balance)

    def test_extend_deadline(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_extend_deadline = Bounty(
            id=6,
            bounty_id=6,
            fulfillmentAmount=1,
            usd_price=1,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_extend_deadline.save()
        bounty_to_extend_deadline_id = bounty_to_extend_deadline.id
        # Extend bounty deadline
        event_timestamp = '1517536922'
        new_deadline_timestamp = '1818636922'
        inputs = {'newDeadline': new_deadline_timestamp}
        bounty_to_extend_deadline = Bounty.objects.get(pk=bounty_to_extend_deadline_id)

        result = self.client.extend_deadline(
            bounty=bounty_to_extend_deadline,
            inputs=inputs,
            event_timestamp=event_timestamp)

        self.assertEqual(result.bountyStage, ACTIVE_STAGE)
        self.assertEqual(result.deadline, datetime(2027, 8, 19, 0, 55, 22))

        bounty_to_extend_deadline_from_db = Bounty.objects.get(
            pk=bounty_to_extend_deadline_id)
        self.assertEqual(result, bounty_to_extend_deadline_from_db)

    def test_change_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_change = Bounty(
            id=7,
            bounty_id=7,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=ACTIVE_STAGE)
        bounty_to_change.save()
        bounty_to_change_id = bounty_to_change.id
        # Change bounty
        bounty_to_change = Bounty.objects.get(pk=bounty_to_change_id)
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL',
            'newDeadline': '1517536923',
            'newFulfillmentAmount': 2,
            'newArbiter': '0x4444444444444444444422222222222222222222'
        }
        new_deadline = datetime.fromtimestamp(int(inputs['newDeadline']))
        result = self.client.change_bounty(
            bounty=bounty_to_change,
            inputs=inputs)
        self.assertEqual(result.deadline, new_deadline)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])
        self.assertEqual(result.arbiter, inputs['newArbiter'])

    def test_transfer_issuer(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_transfer_issuer = Bounty(
            id=8,
            bounty_id=8,
            fulfillmentAmount=1,
            paysTokens=True,
            created=created,
            deadline=deadline,
            issuer='0x4242424242424242424242424242424242424242')
        bounty_to_transfer_issuer.save()
        bounty_to_transfer_issuer_id = bounty_to_transfer_issuer.id
        # Transfer issuer
        bounty_to_transfer_issuer = Bounty.objects.get(pk=bounty_to_transfer_issuer_id)
        inputs = {
            'newIssuer': '0x4444444444444444444422222222222222222222'
        }
        result = self.client.transfer_issuer(
            bounty=bounty_to_transfer_issuer,
            inputs=inputs)
        self.assertEqual(result.issuer, inputs['newIssuer'])
        self.assertNotEqual(result.user.name, result.issuer_name)

    def test_increase_payout(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_increase_payout = Bounty(
            id=9,
            bounty_id=9,
            balance=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            fulfillmentAmount=5)
        bounty_to_increase_payout.save()
        bounty_to_increase_payout_id = bounty_to_increase_payout.id
        # Increase payout without changing balance
        bounty_to_increase_payout = Bounty.objects.get(pk=bounty_to_increase_payout_id)
        old_balance = bounty_to_increase_payout.balance
        inputs = {
            'newFulfillmentAmount': 10
        }
        result = self.client.increase_payout(
            bounty=bounty_to_increase_payout,
            inputs=inputs)
        self.assertEqual(result.balance, old_balance)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])
        # Increase payout and increase balance
        bounty_to_increase_payout = Bounty.objects.get(pk=bounty_to_increase_payout_id)
        old_balance = bounty_to_increase_payout.balance
        inputs = {
            'value': 20,
            'newFulfillmentAmount': 20
        }
        result = self.client.increase_payout(
            bounty=bounty_to_increase_payout,
            inputs=inputs)
        new_balance = old_balance + inputs['value']
        self.assertEqual(result.balance, new_balance)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])
