templates = {
    'BountyIssued': """"{title}, id: {id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_price}
    Deadline: {deadline}
    {link} :tada:
    """,

    'BountyActivated': """{title}, id: {id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_price}
    {link}
    """,

    'BountyFulfilled': """{title}, id: {id}, fulfillment id: {fulfillment_id}
    {link}
    """,

    'FulfillmentUpdated': """{title}, id: {id}, fulfillment id: {fulfillment_id}
    {link}
    """,

    'FulfillmentAccepted': """{title}, id: {id}, fulfillment id: {fulfillment_id}
    ${usd_price}, {total_value} {token_symbol} @ ${token_lock_price}
    Deadline: {deadline}
    {link}
    """,

    'BountyKilled': """{title}, id: {id}
    {link}
    """,

    'ContributionAdded': """{title}, id: {id}
    {link}
    """,

    'DeadlineExtended': """{title}, id: {id}
    new deadline: {deadline}
    {link}
    """,

    'BountyChanged': """{title}, id: {id}
    {link}
    """,

    'IssuerTransferred': """{title}, id: {id}
    {link}
    """,

    'PayoutIncreased': """{title}, id: {id}
    {link}
    """
}
