import random
from datetime import datetime, timedelta
from django.test import TestCase

# Create your tests here.
from std_bounties.constants import EXPIRED_STAGE, DEAD_STAGE, COMPLETED_STAGE, ACTIVE_STAGE, DRAFT_STAGE
from analytics.management.commands.timeline_generator import diff_time, diff_days, day_bounds, range_days, \
    get_bounty_draft, get_bounty_completed, get_bounty_active, get_bounty_expired, get_bounty_dead
from std_bounties.models import BountyState


class DateUtilsTest(TestCase):
    def test_diff_between_two_date(self):
        first_day = datetime(2018, 1, 1, 0, 0)
        last_day = datetime(2019, 1, 1, 0, 0)

        self.assertEqual(diff_time(first_day, last_day), timedelta(365))

    def test_diff_in_days(self):
        first_day = datetime(2018, 1, 1, 0, 0)
        last_day = datetime(2019, 1, 1, 0, 0)

        self.assertEqual(diff_days(first_day, last_day), 365)

    def test_days_bounds(self):
        first_day = datetime(2018, 1, 1, 12, 55)
        (floor, ceil) = day_bounds(first_day)

        self.assertEqual(floor.minute, 0)
        self.assertEqual(floor.hour, 0)
        self.assertEqual(floor.second, 0)
        self.assertEqual(ceil.minute, 23)
        self.assertEqual(ceil.hour, 59)
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


class TestStages(TestCase):
    def setUp(self):
        bounties = [
            *[BountyState(bountyStage=COMPLETED_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=EXPIRED_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=ACTIVE_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=DRAFT_STAGE) for _ in range(1, 20)],
            *[BountyState(bountyStage=DEAD_STAGE) for _ in range(1, 20)]
        ]

        self.bounties = random.shuffle(bounties)

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