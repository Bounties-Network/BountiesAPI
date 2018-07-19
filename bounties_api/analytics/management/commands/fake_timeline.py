from django.core.management import BaseCommand
from faker import Faker


from analytics.models import BountiesTimeline


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        fake.seed(4321)

        for datetime in fake.time_series(
                start_date="-60d",
                end_date="now",
                precision=None,
                distrib=None,
                tzinfo=None):
            b = BountiesTimeline(
                date=fake.past_datetime(datetime[0].date()),
                bounties_issued=abs(fake.pyint()),
                fulfillments_submitted=abs(fake.pyint()),
                fulfillments_accepted=abs(fake.pyint()),
                fulfillments_pending_acceptance=abs(fake.pyint()),
                fulfillment_acceptance_rate=fake.pyfloat(left_digits=3, right_digits=0, positive=True),
                bounty_fulfilled_rate=fake.pyfloat(left_digits=3, right_digits=0, positive=True),
                avg_fulfiller_acceptance_rate=fake.pyfloat(left_digits=3, right_digits=0, positive=True),
                avg_fulfillment_amount=fake.pydecimal(left_digits=2, positive=True),
                total_fulfillment_amount=fake.pydecimal(left_digits=2, positive=True),
                bounty_draft=abs(fake.pyint()),
                bounty_active=abs(fake.pyint()),
                bounty_completed=abs(fake.pyint()),
                bounty_expired=abs(fake.pyint()),
                bounty_dead=abs(fake.pyint()))

            b.save()
