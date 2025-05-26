WITH date_range AS (
    SELECT MIN(date) as min_date,
    SELECT MAX(date) as max_date,
FROM {{ ref('facts_covid_metrics')}}
),


calendar AS (
    SELECT
        dateadd(day, seq4(), (SELECT min_date FROM date_range)) AS date_day
    FROM TABLE(GENERATOR(rowcount => 5000))
    WHERE dateadd(day, seq(), (SELECT min_date FROM date_range)) <= (SELECT max_date FROM date_range)
)


SELECT
    date_day                                                                        AS date,
    EXTRACT(YEAR FROM date_day)                                                     AS year,
    EXTRACT(MONTH FROM date_day)                                                    AS month,
    EXTRACT(DAY FROM date_day)                                                      AS day,
    EXTRACT(DOW FROM date_day)                                                      AS weekday_num,
    EXTRACT(QUARTER from date_day)                                                  AS quarter,
    CASE WHEN EXTRACT(DOW FROM date_day) in (0, 6) THEN TRUE ELSE FALSE END         AS is_weekend,  
    
    -- Month-year expression plus its order for charts
    TO_CHAR(date_day, 'MM-YYYY')                                                    AS month_year,
    EXTRACT(YEAR FROM date_day) * 100 + extract(MONTH from date_day)                AS year_month_order,
    
    -- QUARTER-year expression plus its order for charts
    'Q' || TO_CHAR(date_day, 'Q') || '-' || TO_CHAR(date_day, 'YYYY')               AS quarter_year,
    EXTRACT(YEAR FROM date_day) * 10 + extract(QUARTER FROM date_day)               AS year_quarter_order