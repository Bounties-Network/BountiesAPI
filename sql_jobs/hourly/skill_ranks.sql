CREATE TABLE IF NOT EXISTS skill_ranks (
    id bigint,
    normalized_name varchar(128),
    name varchar(128),
    total_count numeric
);

CREATE TABLE skill_ranks_tmp
AS SELECT * FROM skill_ranks;

DELETE FROM skill_ranks_tmp;

INSERT INTO skill_ranks_tmp
(
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
                        skill_id,
                        count(*) as count
                    FROM user_user_skills
                    GROUP BY skill_id
                ) skill_counts
                JOIN user_skill
                ON user_skill.id = skill_counts.skill_id
                GROUP BY normalized_name
            ) names_and_normalized_counts
            JOIN user_skill
            ON names_and_normalized_counts.normalized_name = user_skill.normalized_name
        ) duplicated_stats
        JOIN (
            SELECT
                name,
                sum(count) as name_count
            FROM (
                SELECT
                    skill_id,
                    count(*) as count
                FROM user_user_skills
                GROUP BY skill_id
            ) skill_counts
            JOIN user_skill
            ON user_skill.id = skill_counts.skill_id
            GROUP BY name
        ) defined_names
        ON duplicated_stats.name = defined_names.name
    ) ranks
    WHERE name_rank = 1 AND name != ''
    ORDER BY total_count desc
);

DROP TABLE IF EXISTS skill_ranks;
ALTER TABLE skill_ranks_tmp RENAME TO skill_ranks;
