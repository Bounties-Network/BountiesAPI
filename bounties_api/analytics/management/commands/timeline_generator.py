from datetime import datetime
from django.core.management import BaseCommand
from analytics.models import BountiesTimeline
from std_bounties.models import BountyState



def diff_time(last_update, param):
    pass


def get_days(last_update, now):
    pass


def day_range(day):
    pass

def group(objects, by):
    return {}


def get_date(time_frame):
    pass


def get_bounties_issued(time_frame):
    pass


def get_fulfillments_submitted(time_frame):
    pass


def get_fulfillments_accepted(time_frame):
    pass


def get_fulfillments_pending_acceptance(time_frame):
    pass


def get_fulfillment_acceptance_rate(time_frame):
    pass


def get_bounty_fulfilled_rate(time_frame):
    pass


def get_avg_fulfiller_acceptance_rate(time_frame):
    pass


def get_avg_fulfillment_amount(time_frame):
    pass


def get_total_fulfillment_amount(time_frame):
    pass


def get_bounty_draft(time_frame):
    pass


def get_bounty_active(time_frame):
    pass


def get_bounty_completed(time_frame):
    pass


def get_bounty_expired(time_frame):
    pass


def get_bounty_dead(time_frame):
    pass

def generate_timeline(time_frame):
    date = get_date(time_frame)
    bounties_issued = get_bounties_issued(time_frame)
    fulfillments_submitted = get_fulfillments_submitted(time_frame)
    fulfillments_accepted = get_fulfillments_accepted(time_frame)
    fulfillments_pending_acceptance = get_fulfillments_pending_acceptance(time_frame)
    fulfillment_acceptance_rate = get_fulfillment_acceptance_rate(time_frame)
    bounty_fulfilled_rate = get_bounty_fulfilled_rate(time_frame)
    avg_fulfiller_acceptance_rate = get_avg_fulfiller_acceptance_rate(time_frame)
    avg_fulfillment_amount = get_avg_fulfillment_amount(time_frame)
    total_fulfillment_amount = get_total_fulfillment_amount(time_frame)
    bounty_draft = get_bounty_draft(time_frame)
    bounty_active = get_bounty_active(time_frame)
    bounty_completed = get_bounty_completed(time_frame)
    bounty_expired = get_bounty_expired(time_frame)
    bounty_dead = get_bounty_dead(time_frame)

    bounty_frame = BountiesTimeline(date=date,
                                    bounties_issued=bounties_issued,
                                    fulfillments_submitted=fulfillments_submitted,
                                    fulfillments_accepted=fulfillments_accepted,
                                    fulfillments_pending_acceptance=fulfillments_pending_acceptance,
                                    fulfillment_acceptance_rate=fulfillment_acceptance_rate,
                                    bounty_fulfilled_rate=bounty_fulfilled_rate,
                                    avg_fulfiller_acceptance_rate=avg_fulfiller_acceptance_rate,
                                    avg_fulfillment_amount=avg_fulfillment_amount,
                                    total_fulfillment_amount=total_fulfillment_amount,
                                    bounty_draft=bounty_draft,
                                    bounty_active=bounty_active,
                                    bounty_completed=bounty_expired,
                                    bounty_expired=bounty_expired,
                                    bounty_dead=bounty_dead)

    return bounty_frame


class TimelineGenerator(BaseCommand):
    def handle(self, *args, **options):
        needs_genesis = not BountiesTimeline.objects.all().count()

        if needs_genesis:
            all_data = BountyState.objects.all()
            bounties_by_day = group(all_data, by='days')

            for day in bounties_by_day:
                bounty_day = generate_timeline(day)

                bounty_day.save()
        else:
            last_update = BountiesTimeline.objects.order_by('date').last()

            days = get_days(last_update, datetime.now)

            # Instead of calculate the last 5 min, we update all day until now
            # this approach provides more flexibility in calculating more stats in the future
            # and provides a better way to expose by day or by hour in case of been needed
            for day in days:
                time_frame = BountyState.objects.filter(change_date__range=day_range(day))
                bounty_day = generate_timeline(time_frame)

                bounty_points = BountiesTimeline.objects.filter(date=day)

                if bounty_points.exist():
                    bounty_point = bounty_points[0]
                    bounty_day.id = bounty_point.id

                bounty_day.save()