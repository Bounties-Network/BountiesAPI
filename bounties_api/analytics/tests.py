import random
from datetime import datetime, timedelta
import unittest

# Create your tests here.
from std_bounties.constants import EXPIRED_STAGE, DEAD_STAGE, COMPLETED_STAGE, ACTIVE_STAGE, DRAFT_STAGE
from analytics.management.commands.timeline_generator import diff_time, diff_days, day_bounds, range_days, \
    get_bounty_draft, get_bounty_completed, get_bounty_active, get_bounty_expired, get_bounty_dead, \
    get_fulfillment_acceptance_rate, get_bounty_fulfilled_rate, get_avg_fulfiller_acceptance_rate, \
    get_avg_fulfillment_amount, get_total_fulfillment_amount, generate_timeline, week_bounds, range_weeks
from std_bounties.models import BountyState, Fulfillment, Bounty


class DateUtilsTest(unittest.TestCase):
    def test_diff_between_two_date(self):
        first_day = datetime(2018, 1, 1, 0, 0)
        last_day = datetime(2019, 1, 1, 0, 0)

        self.assertEqual(diff_time(first_day, last_day), timedelta(365))

    def test_diff_in_days(self):
        first_day = datetime(2018, 1, 1, 0, 0)
        last_day = datetime(2019, 1, 1, 0, 0)

        self.assertEqual(diff_days(first_day, last_day), -365)

    def test_days_bounds(self):
        first_day = datetime(2018, 1, 1, 12, 55)
        (floor, ceil) = day_bounds(first_day)

        self.assertEqual(floor.minute, 0)
        self.assertEqual(floor.hour, 0)
        self.assertEqual(floor.second, 0)
        self.assertEqual(ceil.minute, 59)
        self.assertEqual(ceil.hour, 23)
        self.assertEqual(ceil.second, 59)

    def test_week_bounds(self):
        first_day = datetime(2018, 5, 26, 12, 55)
        (floor, ceil) = week_bounds(first_day)

        self.assertEqual(floor.day, 21)
        self.assertEqual(ceil.day, 27)
        self.assertEqual(floor.minute, 0)
        self.assertEqual(floor.hour, 0)
        self.assertEqual(floor.second, 0)
        self.assertEqual(ceil.minute, 59)
        self.assertEqual(ceil.hour, 23)
        self.assertEqual(ceil.second, 59)

    def test_days_range_between_two_dates(self):
        first_day = datetime(2018, 1, 1, 0, 0)
        last_day = datetime(2018, 12, 31, 11, 59)
        generated_range = range_days(first_day, last_day)
        iterator = iter(generated_range)

        self.assertEqual(len(generated_range), 365)
        for index in range(1, 366):
            day = next(iterator).timetuple().tm_yday
            self.assertEqual(day, index)

    def test_weeks_range_around_two_dates(self):
        first_day = datetime(2018, 1, 5, 0, 0)
        last_day = datetime(2018, 1, 31, 11, 59)
        generated_range = range_weeks(first_day, last_day + timedelta(days=7))
        iterator = iter(generated_range)

        self.assertEqual(len(generated_range), 5)
        for index in range(1, len(generated_range) + 1):
            day = next(iterator).timetuple()
            print(week_bounds(day))
            #self.assertEqual(day, index)
        self.fail()


class TimelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        accepted_date = datetime(2018, 1, 1, 0, 0)
        bounties = [
            Bounty(id=x,
            bounty_id=x, 
            fulfillmentAmount=x,
            usd_price=x,
            deadline=accepted_date,
            paysTokens=True) for x in range(0, 25)
        ]
        bountyStages = [
            *[BountyState(bounty=bounties[x], bountyStage=COMPLETED_STAGE, change_date=accepted_date) for x in range(0, 5)],
            *[BountyState(bounty=bounties[x], bountyStage=EXPIRED_STAGE, change_date=accepted_date) for x in range(5, 10)],
            *[BountyState(bounty=bounties[x], bountyStage=ACTIVE_STAGE, change_date=accepted_date) for x in range(10, 15)],
            *[BountyState(bounty=bounties[x], bountyStage=DRAFT_STAGE, change_date=accepted_date) for x in range(15, 20)],
            *[BountyState(bounty=bounties[x], bountyStage=DEAD_STAGE, change_date=accepted_date) for x in range(20, 25)]
        ]
        fulfillments = [
            Fulfillment(fulfillment_id=x,
            accepted_date=accepted_date if x % 2 == 0 else None,
            bounty=bounties[x],
            fulfiller=x%3,
            accepted=x % 2 == 0,
            fulfillment_created=accepted_date) for x in range(0, 5)
        ]

        for bounty in bounties:
            bounty.save()
        for bountyStage in bountyStages:
            bountyStage.save()
        for fullfilment in fulfillments:
            fullfilment.save()
        

    def test_get_fulfillment_acceptance_rate(self):
        data = Fulfillment.objects.filter(fulfillment_created__lte=datetime(2018, 1, 1, 0, 0))
        self.assertEqual(get_fulfillment_acceptance_rate(data), 0.6)

    def test_get_bounty_fulfilled_rate(self):
        data = Fulfillment.objects.filter(fulfillment_created__lte=datetime(2018, 1, 1, 0, 0))
        bounties = Bounty.objects.all()
        self.assertEqual(get_bounty_fulfilled_rate(data, bounties), 0.2)

    def test_get_avg_fulfiller_acceptance_rate(self):
        data = Fulfillment.objects.filter(fulfillment_created__lte=datetime(2018, 1, 1, 0, 0))
        self.assertAlmostEqual(get_avg_fulfiller_acceptance_rate(data), 0.6666666666666666)

    def test_get_avg_fulfillment_amount(self):
        data = BountyState.objects.filter(change_date__lte=datetime(2018, 1, 1, 0, 0))
        self.assertEqual(get_avg_fulfillment_amount(data), 2.0)

    def test_get_total_fulfillment_amount(self):
        data = BountyState.objects.filter(change_date__lte=datetime(2018, 1, 1, 0, 0))
        self.assertEqual(get_total_fulfillment_amount(data), 10)

    def test_generate_timeline(self):
        result = generate_timeline([datetime(2018, 1, 1, 0, 0), datetime(2018, 1, 1, 0, 0)], 'standardSchema')
        self.assertEqual(result.date, datetime(2018, 1, 1, 0, 0))
        self.assertEqual(result.bounties_issued, 5)
        self.assertEqual(result.bounties_issued_cum, 25)
        self.assertEqual(result.fulfillments_submitted_cum, 5)
        self.assertEqual(result.fulfillments_submitted, 5)
        self.assertEqual(result.fulfillments_accepted_cum, 3)
        self.assertEqual(result.fulfillments_accepted, 3)
        self.assertEqual(result.fulfillments_pending_acceptance, 2)
        self.assertEqual(result.fulfillment_acceptance_rate, 0.6)
        self.assertEqual(result.bounty_fulfilled_rate, 0.25)
        self.assertAlmostEqual(result.avg_fulfiller_acceptance_rate, 0.6666666666666666)
        self.assertEqual(result.avg_fulfillment_amount, 2)
        self.assertEqual(result.total_fulfillment_amount, 10)
        self.assertEqual(result.bounty_draft, 5)
        self.assertEqual(result.bounty_active, 5)
        self.assertEqual(result.bounty_completed, 5)
        self.assertEqual(result.bounty_expired, 5)
        self.assertEqual(result.bounty_dead, 5)
        self.assertEqual(result.schema, 'standardSchema')


class TestStages(unittest.TestCase):
    def setUp(self):
        bounties = [
            *[BountyState(bountyStage=COMPLETED_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=EXPIRED_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=ACTIVE_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=DRAFT_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=DEAD_STAGE) for _ in range(1, 20)]
        ]

        # in place shuffle
        random.shuffle(bounties)
        self.bounties = bounties

    def test_counter_of_bounties_on_completed_stage(self):
        self.assertEqual(get_bounty_completed(self.bounties), 19)

    def test_counter_of_bounties_on_active_stage(self):
        self.assertEqual(get_bounty_active(self.bounties), 19)

    def test_counter_of_bounties_on_expired_stage(self):
        self.assertEqual(get_bounty_expired(self.bounties), 19)

    def test_counter_of_bounties_on_draft_stage(self):
        self.assertEqual(get_bounty_draft(self.bounties), 19)

    def test_counter_of_bounties_on_dead_stage(self):
        self.assertEqual(get_bounty_dead(self.bounties), 19)