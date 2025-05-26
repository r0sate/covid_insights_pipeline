WITH ranked AS (
    SELECT
        location_id,
        date,
        total_cases,
        LAG(total_cases) OVER (PARTITION BY location_id ORDER BY date) AS previous_total
    FROM {{ref('facts_covid_metrics')}})

SELECT *
FROM ranked
WHERE total_cases < previous_total
