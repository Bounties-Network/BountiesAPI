CREATE TABLE category_ranks_tmp
AS (
	SELECT
	 	ROW_NUMBER() over (ORDER BY name) as id,
		normalized_name,
		name,
		total_count
	FROM (
		SELECT
			duplicated_stats.normalized_name,
			defined_names.name,
			total_count,
			name_count,
			ROW_NUMBER() over (partition by normalized_name ORDER BY name_count desc) as name_rank
		FROM(
			SELECT
				name,
				names_and_normalized_counts.normalized_name,
				total_count
			FROM (
				SELECT
					normalized_name,
					sum(count) as total_count
				FROM (
					SELECT
						category_id,
						count(*) as count
					FROM std_bounties_bounty_categories
					GROUP BY category_id
				) category_counts
				JOIN std_bounties_category category
				ON category.id = category_counts.category_id
				GROUP BY normalized_name
			) names_and_normalized_counts
			JOIN std_bounties_category category
			ON names_and_normalized_counts.normalized_name = category.normalized_name
		) duplicated_stats
		JOIN (
			SELECT
				name,
				sum(count) as name_count
			FROM (
				SELECT
					category_id,
					count(*) as count
				FROM std_bounties_bounty_categories
				GROUP BY category_id
			) category_counts
			JOIN std_bounties_category category
			ON category.id = category_counts.category_id
			GROUP BY name
		) defined_names
		ON duplicated_stats.name = defined_names.name
	) ranks
	WHERE name_rank = 1 AND name != ''
	ORDER BY total_count desc
);

DROP TABLE IF EXISTS category_ranks;
ALTER TABLE category_ranks_tmp RENAME TO category_ranks;
