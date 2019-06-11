templates = {
    'BountyIssued': """"{title}, id: {bounty_id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_price}
    Deadline: {deadline}
    {link} :tada:
    """,

    'BountyActivated': """{title}, id: {bounty_id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_price}
    {link}
    """,

    'BountyFulfilled': """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
    {link}
    """,

    'FulfillmentUpdated': """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
    {link}
    """,

    'FulfillmentAccepted': """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_lock_price}
    Deadline: {deadline}
    {link}
    """,

    'BountyKilled': """{title}, id: {bounty_id}
    {link}
    """,

    'ContributionAdded': """{title}, id: {bounty_id}
    {link}
    """,

    'DeadlineExtended': """{title}, id: {bounty_id}
    new deadline: {deadline}
    {link}
    """,

    'BountyChanged': """{title}, id: {bounty_id}
    {link}
    """,

    'IssuerTransferred': """{title}, id: {bounty_id}
    {link}
    """,

    'PayoutIncreased': """{title}, id: {bounty_id}
    {link}
    """
}
