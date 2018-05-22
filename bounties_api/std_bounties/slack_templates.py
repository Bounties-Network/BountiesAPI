BOUNTY_ISSUED_SLACK_STR = """"{title}, id: {bounty_id}
${usd_price}, {total_value} {tokenSymbol} @ ${token_price}
Deadline: {deadline}
{link} :tada:
"""

BOUNTY_ACTIVATED_SLACK_STR = """{title}, id: {bounty_id}
${usd_price}, {total_value} {tokenSymbol} @ ${token_price}
{link}
"""

BOUNTY_FULFILLED_SLACK_STR = """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
{link}
"""

FULFILLMENT_UPDATED_SLACK_STR = """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
{link}
"""

FULFILLMENT_ACCEPTED_SLACK_STR = """{title}, id: {bounty_id}, fulfillment id: {fulfillment_id}
${usd_price}, {total_value} {tokenSymbol} @ ${token_lock_price}
Deadline: {deadline}
{link}
"""

BOUNTY_KILLED_SLACK_STR = """{title}, id: {bounty_id}
{link}
"""

CONTRIBUTION_ADDED_SLACK_STR = """{title}, id: {bounty_id}
{link}
"""

DEADLINE_EXTENDED_SLACK_STR = """{title}, id: {bounty_id}
previous: {previous_deadline}, new deadline: {deadline}
{link}
"""

BOUNTY_CHANGED_SLACK_STR = """{title}, id: {bounty_id}
{link}
"""

ISSUER_TRANSFERRED_SLACK_STR = """{title}, id: {bounty_id}
{link}
"""

PAYOUT_INCREASED_SLACK_STR = """{title}, id: {bounty_id}
{link}
"""
