






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and total_tests >= 0
)
 as expression


    from COVID_DB.dbt_FACT.fct_covid_metrics
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







