# If we used django for this, it would be quite complicated and inefficient.
# By inputting raw SQL - we get a very fast output
LEADERBOARD_FULFILLER_QUERY = """
SELECT
	fulfillment.fulfiller as address,
	profile.name as name,
	profile.email as email,
	profile.github as githubUsername,
	profile.small_profile_image_url as profile_image,
	SUM(bounty."fulfillmentAmount") as total,
	SUM(fulfillment.usd_price) as total_usd,
	COUNT(bounty) as bounties_fulfilled,
	COUNT(fulfillment.id) as fulfillments_accepted
FROM std_bounties_fulfillment fulfillment
JOIN std_bounties_bounty bounty
ON fulfillment.bounty_id = bounty.id
JOIN user_user profile
ON fulfillment.fulfiller = profile.public_address
WHERE fulfillment.accepted = true {}
GROUP BY fulfillment.fulfiller, profile.name, profile.email, profile.github, profile.small_profile_image_url
ORDER BY total_usd desc, total desc
"""


LEADERBOARD_ISSUER_QUERY = """
SELECT
	bounty.issuer as address,
	profile.name as name,
	profile.email as email,
	profile.github as githubUsername,
	profile.small_profile_image_url as profile_image,
	SUM(bounty."fulfillmentAmount") as total,
	SUM(fulfillment.usd_price) as total_usd,
	COUNT(distinct(bounty.id)) as bounties_issued,
	COUNT(fulfillment) as fulfillments_paid
FROM std_bounties_fulfillment fulfillment
JOIN std_bounties_bounty bounty
ON fulfillment.bounty_id = bounty.id
JOIN user_user profile
ON bounty.issuer = profile.public_address
WHERE fulfillment.accepted = true {}
GROUP BY bounty.issuer, profile.name, profile.email, profile.github, profile.small_profile_image_url
ORDER BY total_usd desc, total desc
"""
