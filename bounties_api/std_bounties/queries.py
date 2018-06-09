# If we used django for this, it would be quite complicated and inefficient.
# By inputting raw SQL - we get a very fast output
LEADERBOARD_FULFILLER_QUERY = """
SELECT
	fulfillment.fulfiller as address,
	fulfillment_profiles.fulfiller_name as name,
	fulfillment_profiles.fulfiller_email as email,
	fulfillment_profiles."fulfiller_githubUsername" as githubUsername,
	SUM(bounty."fulfillmentAmount") as total,
	SUM(fulfillment.usd_price) as total_usd,
	COUNT(bounty) as bounties_fulfilled,
	COUNT(fulfillment.id) as fulfillments_accepted
FROM std_bounties_fulfillment fulfillment
JOIN std_bounties_bounty bounty
ON fulfillment.bounty_id = bounty.id
JOIN
(
	SELECT
		fulfillments.fulfiller,
		fulfiller_name,
		fulfiller_email,
		"fulfiller_githubUsername"
	FROM std_bounties_fulfillment fulfillments
	INNER JOIN (
		SELECT
			fulfiller,
			MAX(created) as max_date
		FROM std_bounties_fulfillment
		WHERE std_bounties_fulfillment.fulfiller_name != ''
		GROUP BY fulfiller
		UNION
		(
			SELECT
				without_name.fulfiller,
				without_name.max_date
			FROM (
				SELECT
					fulfiller,
					MAX(created) as max_date
				FROM std_bounties_fulfillment
				WHERE fulfiller_name != ''
				GROUP BY fulfiller
			) with_name
			RIGHT JOIN
			(
				SELECT
					fulfiller,
					MAX(created) as max_date
				FROM std_bounties_fulfillment
				WHERE fulfiller_name = ''
				GROUP BY fulfiller
			) without_name
			ON with_name.fulfiller = without_name.fulfiller
			WHERE with_name.fulfiller IS NULL
		)
	) max_date_fulfillment
	ON fulfillments.fulfiller = max_date_fulfillment.fulfiller
		AND fulfillments.created = max_date_fulfillment.max_date
) fulfillment_profiles
ON fulfillment.fulfiller = fulfillment_profiles.fulfiller
WHERE fulfillment.accepted = true {}
GROUP BY fulfillment.fulfiller, fulfillment_profiles.fulfiller_name, fulfillment_profiles.fulfiller_email, fulfillment_profiles."fulfiller_githubUsername"
ORDER BY total_usd desc, total desc
"""


LEADERBOARD_ISSUER_QUERY = """
SELECT
	bounty.issuer as address,
	bounty_profiles.issuer_name as name,
	bounty_profiles.issuer_email as email,
	bounty_profiles."issuer_githubUsername" as githubUsername,
	SUM(bounty."fulfillmentAmount") as total,
	SUM(fulfillment.usd_price) as total_usd,
	COUNT(distinct(bounty.id)) as bounties_issued,
	COUNT(fulfillment) as fulfillments_paid
FROM std_bounties_fulfillment fulfillment
JOIN std_bounties_bounty bounty
ON fulfillment.bounty_id = bounty.id
JOIN
(
	SELECT
		bounties.issuer,
		issuer_name,
		issuer_email,
		"issuer_githubUsername"
	FROM std_bounties_bounty bounties
	INNER JOIN (
		SELECT
			issuer,
			MAX(created) as max_date
		FROM std_bounties_bounty
		WHERE issuer_name != ''
		GROUP BY issuer
		UNION
		(
			SELECT
				without_name.issuer,
				without_name.max_date
			FROM (
				SELECT
					issuer,
					MAX(created) as max_date
				FROM std_bounties_bounty
				WHERE issuer_name != ''
				GROUP BY issuer
			) with_name
			RIGHT JOIN
			(
				SELECT
					issuer,
					MAX(created) as max_date
				FROM std_bounties_bounty
				WHERE issuer_name = ''
				GROUP BY issuer
			) without_name
			ON with_name.issuer = without_name.issuer
			WHERE with_name.issuer IS NULL
		)
	) max_date_bounty
	ON bounties.issuer = max_date_bounty.issuer
		AND bounties.created = max_date_bounty.max_date
) bounty_profiles
ON bounty.issuer = bounty_profiles.issuer
WHERE fulfillment.accepted = true {}
GROUP BY bounty.issuer, bounty_profiles.issuer_name, bounty_profiles.issuer_email, bounty_profiles."issuer_githubUsername"
ORDER BY total_usd desc, total desc
"""
