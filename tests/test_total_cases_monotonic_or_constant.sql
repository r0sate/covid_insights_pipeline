WITH ranked AS (
    SELECT
        iso_code,
        date,
        total_cases,
        LAG(total_cases) OVER (PARTITION BY iso_code ORDER BY date) AS previous_total
    FROM {{ref('facts_covid_metrics')}})

SELECT *
FROM ranked
WHERE total_cases <= previous_total
