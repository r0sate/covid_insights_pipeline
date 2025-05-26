
  
    

create or replace transient table COVID_DB.dbt_DIM.dim_location_type
    

    
    as (SELECT *
FROM (
    VALUES
        (0, 'Country'),
        (1, 'Aggregated Region')
) AS t(location_type, description)
    )
;


  