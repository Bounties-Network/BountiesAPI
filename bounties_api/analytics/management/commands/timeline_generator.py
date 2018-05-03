from datetime import datetime, timedelta
from functools import reduce

import arrow
from django.core.management import BaseCommand

from analytics.models import BountiesTimeline
from std_bounties.constants import EXPIRED_STAGE, DEAD_STAGE, COMPLETED_STAGE, ACTIVE_STAGE, DRAFT_STAGE
from std_bounties.models import BountyState, Fulfillment, Bounty


def diff_time(since, until):
    return until - since


def diff_days(last_update, now=datetime.utcnow()):
    return (diff_time(now, last_update)).days


def day_bounds(day):
    utc_day = arrow.get(day).to('utc')
    floor = utc_day.floor('day')
    ceil = utc_day.ceil('day')

    return floor.datetime, ceil.datetime


def range_days(since, until):
    return arrow.Arrow.range('day', since, until)


def get_date(time_frame):
    return time_frame.last().change_date


def add_on(stage):
    return lambda current, next_value: current + 1 if next_value.bountyStage == stage else current


def get_bounties_issued(time_frame):
    return time_frame.distinct('bounty').count()


def get_fulfillments_submitted(time_frame):
    return time_frame.count()


def get_fulfillments_accepted(time_frame):
    return time_frame.count()


def get_fulfillment_acceptance_rate(time_frame, accepted_date=datetime.now()):
    return time_frame.filter(accepted_date__lte=accepted_date).count() / time_frame.count()


def get_bounty_fulfilled_rate(time_frame, bounties):
    return time_frame.distinct('bounty').count() / bounties.count()


def get_avg_fulfiller_acceptance_rate(time_frame, accepted_date=datetime.now()):
    fulfillers = [b['fulfiller'] for b in time_frame.values('fulfiller').distinct()]
    counter = 0
    accumulator = 0

    for fulfiller in fulfillers:
        fulfillments = time_frame.filter(fulfiller=fulfiller)
        accepted_fulfillments = fulfillments.filter(accepted=True, accepted_date__lte=accepted_date).count()
        accumulator += accepted_fulfillments / fulfillments.count()
        counter += 1

    return accumulator / counter if counter > 0 else 0


def get_avg_fulfillment_amount(time_frame):
    completed_bounties = filter(lambda bounty: bounty.bountyStage == COMPLETED_STAGE, time_frame)
    (total, count) = reduce(lambda prev, current: (prev[0] + current.bounty.usd_price, prev[1] + 1),
                            completed_bounties,
                            (0, 0))

    return total / count if count > 0 else 0


def get_total_fulfillment_amount(time_frame):
    completed_bounties = filter(lambda bounty: bounty.bountyStage == COMPLETED_STAGE, time_frame)
    return reduce(lambda prev, current: prev + current.bounty.fulfillmentAmount, completed_bounties, 0)


def get_bounty_draft(time_frame):
    return reduce(add_on(DRAFT_STAGE), time_frame, 0)


def get_bounty_active(time_frame):
    return reduce(add_on(ACTIVE_STAGE), time_frame, 0)


def get_bounty_completed(time_frame):
    return reduce(add_on(COMPLETED_STAGE), time_frame, 0)


def get_bounty_expired(time_frame):
    return reduce(add_on(EXPIRED_STAGE), time_frame, 0)


def get_bounty_dead(time_frame):
    return reduce(add_on(DEAD_STAGE), time_frame, 0)


def build_stages(time_frame):
    """ Build the total for each bounty stage in a given time frame

    1. In a given time frame, are retrieved all distinct bounties
    2. Get the last stage for the bounty
    3. Increment the counter for the given stage

    Each position correspond in the stage array correspond to the stage in `constants.py`:
        DRAFT_STAGE = 0
        ACTIVE_STAGE = 1
        DEAD_STAGE = 2
        COMPLETED_STAGE = 3
        EXPIRED_STAGE = 4

    returns [total_drafts, total_active, total_dead, total_completed, total_expired]

    **Each total correspond to the last stages of the bounties in the given time frame**
    """
    # TODO: Queries optimization
    unique_bounties = [b['bounty'] for b in time_frame.values('bounty').distinct()]

    stages = [0, 0, 0, 0, 0]

    for bounty_id in unique_bounties:
        current_stage = time_frame.filter(bounty=bounty_id).order_by('-change_date').first().bountyStage
        stages[current_stage] = stages[current_stage] + 1

    return stages


def generate_timeline(time_frame):
    date = time_frame[1]
    bounties_state_frame_day = BountyState.objects.filter(change_date__range=time_frame, bountyStage=DRAFT_STAGE)
    bounties_state_frame = BountyState.objects.filter(change_date__lte=time_frame[1])
    fulfillment_accepted_frame = Fulfillment.objects.filter(accepted_date__lte=time_frame[1])
    fulfillment_accepted_frame_day = Fulfillment.objects.filter(accepted_date__range=time_frame)
    fulfillment_submitted_frame = Fulfillment.objects.filter(fulfillment_created__lte=time_frame[1])
    fulfillment_submitted_frame_day = Fulfillment.objects.filter(fulfillment_created__range=time_frame)

    stages = build_stages(bounties_state_frame)

    bounties_issued = get_bounties_issued(bounties_state_frame_day)
    bounties_issued_cum = get_bounties_issued(bounties_state_frame)

    fulfillments_submitted = get_fulfillments_submitted(fulfillment_submitted_frame_day)
    fulfillments_submitted_cum = get_fulfillments_submitted(fulfillment_submitted_frame)

    fulfillments_accepted = get_fulfillments_accepted(fulfillment_accepted_frame_day)
    fulfillments_accepted_cum = get_fulfillments_accepted(fulfillment_accepted_frame)

    fulfillment_acceptance_rate = get_fulfillment_acceptance_rate(fulfillment_submitted_frame, date)

    bounty_fulfilled_rate = get_bounty_fulfilled_rate(fulfillment_submitted_frame,
                                                      bounties_state_frame.distinct('bounty'))

    avg_fulfiller_acceptance_rate = get_avg_fulfiller_acceptance_rate(fulfillment_submitted_frame, date)

    avg_fulfillment_amount = get_avg_fulfillment_amount(bounties_state_frame)
    total_fulfillment_amount = get_total_fulfillment_amount(bounties_state_frame)

    bounty_frame = BountiesTimeline(date=date,
                                    bounties_issued=bounties_issued,
                                    bounties_issued_cum=bounties_issued_cum,
                                    fulfillments_submitted_cum=fulfillments_submitted_cum,
                                    fulfillments_submitted=fulfillments_submitted,
                                    fulfillments_accepted_cum=fulfillments_accepted_cum,
                                    fulfillments_accepted=fulfillments_accepted,
                                    fulfillments_pending_acceptance=fulfillments_submitted_cum - fulfillments_accepted_cum,
                                    fulfillment_acceptance_rate=fulfillment_acceptance_rate,
                                    bounty_fulfilled_rate=bounty_fulfilled_rate,
                                    avg_fulfiller_acceptance_rate=avg_fulfiller_acceptance_rate,
                                    avg_fulfillment_amount=avg_fulfillment_amount,
                                    total_fulfillment_amount=total_fulfillment_amount,
                                    bounty_draft=stages[DRAFT_STAGE],
                                    bounty_active=stages[ACTIVE_STAGE],
                                    bounty_completed=stages[COMPLETED_STAGE],
                                    bounty_expired=stages[EXPIRED_STAGE],
                                    bounty_dead=stages[DEAD_STAGE])

    return bounty_frame


class Command(BaseCommand):
    def handle(self, *args, **options):
        needs_genesis = not BountiesTimeline.objects.all().count()

        if needs_genesis:
            first_date = BountyState.objects.first()
            last_date = BountyState.objects.last()

            bounties_by_day = range_days(first_date.change_date, last_date.change_date + timedelta(days=1))

            for day in bounties_by_day:
                bounty_day = generate_timeline(day_bounds(day))

                bounty_day.save()
        else:
            last_update = BountiesTimeline.objects.order_by('date').last()
            since = arrow.get(last_update.date).to('utc')
            days = range_days(since, datetime.utcnow())

            # Instead of calculate the last 5 min, we update all day until now
            # this approach provides more flexibility and simplicity in calculating more stats in the future
            # and provides a better way to expose by day or by hour in case of been needed
            for day in days:
                bounty_day = generate_timeline(day_bounds(day))
                bounty_points = BountiesTimeline.objects.filter(date=day.date())

                if bounty_points.exists():
                    bounty_point = bounty_points.first()
                    bounty_day.id = bounty_point.id

                bounty_day.save()