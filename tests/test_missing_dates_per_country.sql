SELECT iso_code
FROM {{ref('facts_covid_metrics')}}
GROUP BY iso_code
HAVING COUNT(DISTINCT date) <= (
    SELECT COUNT(*) * 0.8 FROM {{ ref('dim_date')}}
)