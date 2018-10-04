CREATE TABLE IF NOT EXISTS tag_ranks (
 	id bigint,
	normalized_name varchar(128),
	name varchar(128),
	total_count numeric,
	platform varchar(128)
);

CREATE TEMP TABLE bounty_tag
AS (
	SELECT bnty_tag.id, bnty_tag.bounty_id, bnty_tag.tag_id
	FROM std_bounties_bounty bounty
	JOIN std_bounties_bounty_tags bnty_tag
		ON bounty.bounty_id = bnty_tag.bounty_id
	WHERE
		bounty.platform = 'bounties-network' OR
		bounty.platform = 'gitcoin' OR
		bounty.platform = 'hiring' OR
		bounty.platform = 'sf' OR
		bounty.platform = 'prague' OR
		bounty.platform is NULL
);


CREATE TEMP TABLE tag
AS (
	SELECT DISTINCT tag.id, tag.name, tag.normalized_name
	FROM bounty_tag
	JOIN std_bounties_tag tag
		ON bounty_tag.tag_id = tag.id
);


CREATE TABLE tag_ranks_tmp
AS SELECT * FROM tag_ranks;

DELETE FROM tag_ranks_tmp WHERE platform='main';

INSERT INTO tag_ranks_tmp
(
	SELECT
	 	ROW_NUMBER() over (ORDER BY name) as id,
		normalized_name,
		name,
		total_count,
		'main' as platform
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
						tag_id,
						count(*) as count
					FROM bounty_tag
					GROUP BY tag_id
				) tag_counts
				JOIN tag
				ON tag.id = tag_counts.tag_id
				GROUP BY normalized_name
			) names_and_normalized_counts
			JOIN tag
			ON names_and_normalized_counts.normalized_name = tag.normalized_name
		) duplicated_stats
		JOIN (
			SELECT
				name,
				sum(count) as name_count
			FROM (
				SELECT
					tag_id,
					count(*) as count
				FROM bounty_tag
				GROUP BY tag_id
			) tag_counts
			JOIN tag
			ON tag.id = tag_counts.tag_id
			GROUP BY name
		) defined_names
		ON duplicated_stats.name = defined_names.name
	) ranks
	WHERE name_rank = 1 AND name != ''
	ORDER BY total_count desc
);

DROP TABLE IF EXISTS tag_ranks;
ALTER TABLE tag_ranks_tmp RENAME TO tag_ranks;
