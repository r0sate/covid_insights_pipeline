SELECT location_id
FROM {{ref('facts_covid_metrics')}}
GROUP BY location_id
HAVING COUNT(DISTINCT date) < (
    SELECT COUNT(*) FROM {{ ref('dim_date')}}
)