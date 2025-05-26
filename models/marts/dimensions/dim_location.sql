WITH valid_countries as (
    SELECT
        iso_code,
        location,
        continent,
        0 AS location_type
    FROM {{ref('stg_owid_covid_data')}}
    WHERE continent IS NOT NULL
    AND iso_code NOT LIKE 'OWID_%'
),
aggregated_regions AS (
    SELECT
        iso_code,
        location,
        null as continent,
        1 as location_type
        FROM {{ref('stg_owid_covid_data')}}
        WHERE iso_code LIKE 'OWID_%'
)

SELECT * FROM valid_countries
UNION ALL
SELECT * FROM aggregated_regions
