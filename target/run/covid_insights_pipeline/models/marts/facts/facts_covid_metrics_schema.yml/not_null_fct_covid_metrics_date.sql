
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date
from COVID_DB.dbt_FACT.fct_covid_metrics
where date is null



  
  
      
    ) dbt_internal_test