from std_bounties.models import Fulfillment, Bounty, BountyState
from std_bounties.constants import ACTIVE_STAGE
from notifications.models import Notification, DashboardNotification
from notifications.constants import *
from notifications.notification_helpers import createDashboardNotification
from notifications.notification_templates import *
from .base_clients import BaseClient


class NotificationClient(BaseClient):
    def __init__(self):
        pass

    def fulfillment_submitted(self, bounty, fulfillment_id):
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty=bounty)
        string_data_fulfiller = FULFILLMENT_SUBMITTED_FULFILLER_STR.format(bounty_title=bounty.title)
        string_data_issuer = FULFILLMENT_SUBMITTED_ISSUER_STR.format(bounty_title=bounty.title)
        # to fulfiller
        createDashboardNotification(FULFILLMENT_SUBMITTED, fulfillment.user, fulfillment.fulfillment_created, string_data_fulfiller)
        # to bounty issuer
        createDashboardNotification(FULFILLMENT_SUBMITTED, bounty.user, fulfillment.fulfillment_created, string_data_issuer)
        # Once we include email, email client call added here

    def bounty_activated(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_ACTIVATED_STR.format(bounty_title=bounty.title)
        createDashboardNotification(BOUNTY_ACTIVATED, bounty.user, bounty_state.change_date, string_data)

    def fulfillment_accepted(self, bounty, fulfillment_id):
        fulfillment = Fulfillment.objects.get(bounty_id=bounty, fulfillment_id=fulfillment_id)
        string_data = FULFILLMENT_ACCEPTED_STR.format(bounty_title=bounty.title)
        createDashboardNotification(FULFILLMENT_ACCEPTED, bounty.user, fulfillment.accepted_date, string_data)

    def bounty_expired(self, bounty):
        bounty_state = BountyState.objects.filter(bounty=bounty, bountyStage=ACTIVE_STAGE).latest()
        string_data = BOUNTY_EXPIRED_STR.format(bounty_title=bounty.title)
        createDashboardNotification(BOUNTY_EXPIRED, bounty.user, bounty_state.change_date, string_data)
