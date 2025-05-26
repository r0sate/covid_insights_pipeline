
    
    

with child as (
    select location_id as from_field
    from COVID_DB.dbt_FACT.fct_covid_metrics
    where location_id is not null
),

parent as (
    select location_id as to_field
    from COVID_DB.dbt_DIM.dim_location
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


