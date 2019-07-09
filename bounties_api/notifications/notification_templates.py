notification_templates = {
    'BountyIssued': 'You issued a bounty for: {bounty_title}.',
    'FulfillmentSubmitted': 'You made a submission to: {bounty_title}.',
    'FulfillmentSubmittedIssuer': 'You have a pending submission for: {bounty_title}.',
    'BountyActivated': 'Your Bounty Has Been Released to the Wild: {bounty_title}.',
    'FulfillmentAcceptedFulfiller': 'Your submission has been accepted for: {bounty_title}.',
    'FulfillmentAccepted': 'You accepted a submission for: {bounty_title}.',
    'FulfillmentUpdatedIssuer': 'A submission was updated for bounty: {bounty_title}.',
    'FulfillmentUpdated': 'You made an update to your submission on: {bounty_title}.',
    'BountyKilled': 'You killed: {bounty_title}.',
    'ContributionAdded': 'You contributed {amount} to: {bounty_title}.',
    'DeadlineExtended': 'You extended the deadline of: {bounty_title}.',
    'BountyChanged': 'The bounty you submitted to has been updated: {bounty_title}.',
    'BountyChangedIssuer': 'You updated your bounty: {bounty_title}.',
    'IssuerTransferred': 'You transferred ownership of: {bounty_title}.',
    'TransferredRecipient': 'You are now the owner of: {bounty_title}.',
    'PayoutIncreased': 'You increased the payout of: {bounty_title}.',
    'BountyExpired': 'Yikes! Your bounty has expired: {bounty_title}.',
    'BountyCommentReceived': 'A comment was added for the bounty: {bounty_title}.',
    'RatingReceived': 'You received a review for your experience with: {bounty_title}.',
    'RatingIssued': 'You left a review for your experience with: {bounty_title}.',
    'ProfileUpdated': 'You updated your profile assciated with: {public_address}.',
    'BountyComment': 'You wrote a comment for: {bounty_title}.',
    'DraftCreated': 'You created draft {draft_id}.',
    'DraftUpdated': 'You updated draft {draft_id}.',
    'ContributionReceived': '{bounty_title} received {amount} in contribution',
    'BountyCompleted': '{bounty_title} is out of funds',
    'ApplicationCreated': 'You applied to: {bounty_title}',
    'ApplicationReceived': 'You received an application to your bounty: {bounty_title}',
    'ApplicationAcceptedApplicant': 'Your application was accepted for: {bounty_title}',
    'ApplicationAcceptedIssuer': 'You accepted an application for: {bounty_title}',
    'ApplicationRejectedApplicant': 'Your application was rejected for: {bounty_title}',
    'ApplicationRejectedIssuer': 'You rejected an application for: {bounty_title}',
    'BountyCommentReceivedIssuer': 'A comment was added for your bounty: {bounty_title}.',
    'BountyChangedApplicant': 'The bounty you applied to has been updated: {bounty_title}.',
    'BountyCommentReceivedCommenter': 'A comment was added for the bounty: {bounty_title}.',
    'FulfillmentCommentReceived': 'A comment was added to your submission for the bounty: {bounty_title}.',
    'FulfillmentCommentReceivedIssuer': 'A comment was added to a submission for the bounty: {bounty_title}.',
    'FulfillmentCommentReceivedCommenter': 'A comment was added for a submission to the bounty: {bounty_title}.',
}

email_templates = {
    'FulfillmentAcceptedFulfiller': """Your bounty submission to: {bounty_title} was accepted and your payment was processed!
    If you would like, you can rate your experience with the bounty issuer.  This will help set
    expectations for others on the platform.
    """,
    'FulfillmentAccepted': """You accepted a submission to: {bounty_title} and your payment was processed! If you would like, you can rate your experience with the bounty hunter.  This will help set
    expectations for others on the platform.
    """
}
