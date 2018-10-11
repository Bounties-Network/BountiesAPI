CREATE TABLE IF NOT EXISTS category_ranks (
    id bigint,
    normalized_name varchar(128),
    name varchar(128),
    total_count numeric,
    platform varchar(128)
);

CREATE TEMP TABLE bounty_category
AS (
    SELECT bnty_category.id, bnty_category.bounty_id, bnty_category.category_id
    FROM std_bounties_bounty bounty
    JOIN std_bounties_bounty_categories bnty_category
        ON bounty.bounty_id = bnty_category.bounty_id
    WHERE
        bounty.platform = 'pollenbees'
);


CREATE TEMP TABLE category 
AS (
    SELECT DISTINCT category.id, category.name, category.normalized_name
    FROM bounty_category
    JOIN std_bounties_category category
        ON bounty_category.category_id = category.id
);


CREATE TABLE category_ranks_tmp
AS SELECT * FROM category_ranks;

DELETE FROM category_ranks_tmp WHERE platform='pollenbees';

INSERT INTO category_ranks_tmp
(
    SELECT
        ROW_NUMBER() over (ORDER BY name) as id,
        normalized_name,
        name,
        total_count,
        'pollenbees' as platform
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
                    FROM bounty_category
                    GROUP BY category_id
                ) category_counts
                JOIN category
                ON category.id = category_counts.category_id
                GROUP BY normalized_name
            ) names_and_normalized_counts
            JOIN category
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
                FROM bounty_category
                GROUP BY category_id
            ) category_counts
            JOIN category
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
