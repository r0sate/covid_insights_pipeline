SELECT location_id
FROM COVID_DB.dbt_FACT.fct_covid_metrics
GROUP BY location_id
HAVING COUNT(DISTINCT date) < (
    SELECT COUNT(*) FROM COVID_DB.dbt_DIM.dim_date
)