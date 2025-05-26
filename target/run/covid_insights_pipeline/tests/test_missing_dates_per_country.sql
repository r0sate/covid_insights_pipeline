
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT location_id
FROM COVID_DB.dbt_FACT.fct_covid_metrics
GROUP BY location_id
HAVING COUNT(DISTINCT date) < (
    SELECT COUNT(*) FROM COVID_DB.dbt_DIM.dim_date
)
  
  
      
    ) dbt_internal_test