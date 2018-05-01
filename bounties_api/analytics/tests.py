from datetime import datetime, timedelta
from django.test import TestCase

# Create your tests here.
from analytics.management.commands.timeline_generator import diff_time, diff_days, day_bounds, range_days


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
