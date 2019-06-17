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
BOUNTY_COMMENT_RECEIVED = 15
BOUNTY_ISSUED_ACTIVATED = 16
FULFILLMENT_UPDATED = 17
FULFILLMENT_UPDATED_ISSUER = 18
RATING_ISSUED = 19
RATING_RECEIVED = 20
PROFILE_UPDATED = 21
BOUNTY_COMMENT = 22
DRAFT_CREATED = 23
DRAFT_UPDATED = 24
CONTRIBUTION_RECEIVED = 25
BOUNTY_COMPLETED = 26
APPLICATION_CREATED = 27
APPLICATION_RECEIVED = 28
APPLICATION_ACCEPTED_APPLICANT = 29
APPLICATION_ACCEPTED_ISSUER = 30
APPLICATION_REJECTED_APPLICANT = 31
APPLICATION_REJECTED_ISSUER = 32
BOUNTY_COMMENT_RECEIVED_ISSUER = 33
BOUNTY_CHANGED_APPLICANT = 34
BOUNTY_COMMENT_RECEIVED_COMMENTER = 35

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
    (BOUNTY_COMMENT_RECEIVED, 'BountyCommentReceived'),
    (BOUNTY_ISSUED_ACTIVATED, 'BountyIssuedActivated'),
    (FULFILLMENT_UPDATED, 'FulfillmentUpdated'),
    (FULFILLMENT_UPDATED_ISSUER, 'FulfillmentUpdatedIssuer'),
    (RATING_ISSUED, 'RatingIssued'),
    (RATING_RECEIVED, 'RatingReceived'),
    (PROFILE_UPDATED, 'ProfileUpdated'),
    (BOUNTY_COMMENT, 'BountyComment'),
    (DRAFT_CREATED, 'DraftCreated'),
    (DRAFT_UPDATED, 'DraftUpdated'),
    (CONTRIBUTION_RECEIVED, 'ContributionReceived'),
    (BOUNTY_COMPLETED, 'BountyCompleted'),
    (APPLICATION_CREATED, 'ApplicationCreated'),
    (APPLICATION_RECEIVED, 'ApplicationReceived'),
    (APPLICATION_ACCEPTED_APPLICANT, 'ApplicationAcceptedApplicant'),
    (APPLICATION_ACCEPTED_ISSUER, 'ApplicationAcceptedIssuer'),
    (APPLICATION_REJECTED_APPLICANT, 'ApplicationRejectedApplicant'),
    (APPLICATION_REJECTED_ISSUER, 'ApplicationRejectedIssuer'),
    (BOUNTY_COMMENT_RECEIVED_ISSUER, 'BountyCommentReceivedIssuer'),
    (BOUNTY_COMMENT_RECEIVED_COMMENTER, 'BountyCommentReceivedCommenter'),
    (BOUNTY_CHANGED_APPLICANT, 'BountyChangedApplicant'),
)

id_to_notification = dict(NOTIFICATION_IDS)
notifications = dict((y, x) for x, y in NOTIFICATION_IDS)

push_notification_options = {
    'issuer': [
        id_to_notification[notif] for notif in [
            FULFILLMENT_SUBMITTED_ISSUER,
            FULFILLMENT_UPDATED_ISSUER,
            TRANSFER_RECIPIENT,
            BOUNTY_EXPIRED,
            BOUNTY_COMMENT_RECEIVED_ISSUER,
            CONTRIBUTION_RECEIVED,
            BOUNTY_COMPLETED,
            APPLICATION_RECEIVED,
        ]],
    'fulfiller': [
        id_to_notification[notif] for notif in [
            FULFILLMENT_ACCEPTED_FULFILLER,
            APPLICATION_ACCEPTED_APPLICANT,
            APPLICATION_REJECTED_APPLICANT,
            BOUNTY_CHANGED_APPLICANT,
            BOUNTY_CHANGED,
            BOUNTY_COMMENT_RECEIVED_COMMENTER,
            BOUNTY_COMMENT_RECEIVED,
        ]],
    'both': [
        id_to_notification[notif] for notif in [RATING_RECEIVED]],
}

default_email_options = {
    'activity': False,
    'issuer': {notif: True for notif in push_notification_options['issuer']},
    'fulfiller': {notif: True for notif in push_notification_options['fulfiller']},
    'both': {notif: True for notif in push_notification_options['both']},
}
