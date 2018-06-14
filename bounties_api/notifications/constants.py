FULFILLMENT_SUBMITTED = 0
FULFILLMENT_SUBMITTED_ISSUER = 1
BOUNTY_ACTIVATED = 2
FULFILLMENT_ACCEPTED = 3
FULFILLMENT_ACCEPTED_FULFILLER = 4
BOUNTY_EXPIRED = 5
BOUNTY_ISSUED = 6
BOUNTY_KILLED = 7
CONTRIBUTION_ADDED = 8
DEADLINE_EXTENDED = 9
BOUNTY_CHANGED = 10
ISSUER_TRANSFERRED = 11
TRANSFER_RECIPIENT = 12
PAYOUT_INCREASED = 13
BOUNTY_EXPIRED = 14
BOUNTY_COMMENT = 15
BOUNTY_ISSUED_ACTIVATED = 16
FULFILLMENT_UPDATED = 17
FULFILLMENT_UPDATED_ISSUER = 18
RATING_ISSUED = 19
RATING_RECEIVED = 20

NOTIFICATION_IDS = (
    (FULFILLMENT_SUBMITTED, 'FulfillmentSubmitted'),
    (FULFILLMENT_SUBMITTED_ISSUER, 'FulfillmentSubmittedIssuer'),
    (BOUNTY_ACTIVATED, 'BountyActivated'),
    (FULFILLMENT_ACCEPTED, 'FulfillmentAccepted'),
    (FULFILLMENT_ACCEPTED_FULFILLER, 'FulfillmentAcceptedFulfiller'),
    (BOUNTY_EXPIRED, 'BountyExpired'),
    (BOUNTY_ISSUED, 'BountyIssued'),
    (BOUNTY_KILLED, 'BountyKilled'),
    (CONTRIBUTION_ADDED, 'ContributionAdded'),
    (DEADLINE_EXTENDED, 'DeadlineExtended'),
    (BOUNTY_CHANGED, 'BountyChanged'),
    (ISSUER_TRANSFERRED, 'IssuerTransferred'),
    (TRANSFER_RECIPIENT, 'TransferRecipient'),
    (PAYOUT_INCREASED, 'PayoutIncreased'),
    (BOUNTY_EXPIRED, 'BountyExpired'),
    (BOUNTY_COMMENT, 'BountyComment'),
    (BOUNTY_ISSUED_ACTIVATED, 'BountyIssuedActivated'),
    (FULFILLMENT_UPDATED, 'FulfillmentUpdated'),
    (FULFILLMENT_UPDATED_ISSUER, 'FulfillmentUpdatedIssuer'),
    (RATING_ISSUED, 'RatingIssued'),
    (RATING_RECEIVED, 'RatingReceived'),
)

mapped_notifications = dict(NOTIFICATION_IDS)
rev_mapped_notifications =  dict((y, x) for x, y in NOTIFICATION_IDS)

push_notification_options = {
    'issuer': [mapped_notifications[notif] for notif in [FULFILLMENT_SUBMITTED_ISSUER, FULFILLMENT_UPDATED_ISSUER, TRANSFER_RECIPIENT, BOUNTY_EXPIRED, BOUNTY_COMMENT]],
    'fulfiller': [mapped_notifications[notif] for notif in [FULFILLMENT_ACCEPTED_FULFILLER]],
    'both': [mapped_notifications[notif] for notif in [RATING_ISSUED]],
}

default_email_options = {
    'activity': True,
    'issuer': { notif: True for notif in push_notification_options['issuer']},
    'fulfiller': { notif: True for notif in push_notification_options['fulfiller']},
    'both': { notif: True for notif in push_notification_options['both']},
}
