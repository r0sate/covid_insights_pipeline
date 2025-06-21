WITH valid_countries AS (
    SELECT DISTINCT
        iso_code,
        location,
        continent,
        CAST(0 AS NUMBER) AS location_type
    FROM {{ ref('stg_owid_covid_data') }}
    WHERE continent IS NOT NULL
      AND iso_code NOT LIKE 'OWID_%'
),
aggregated_regions AS (
    SELECT DISTINCT
        iso_code,
        location,
        CAST(NULL AS VARCHAR) AS continent,
        CAST(1 AS NUMBER) AS location_type
    FROM {{ ref('stg_owid_covid_data') }}
    WHERE iso_code LIKE 'OWID_%'
)

SELECT * FROM valid_countries
UNION
SELECT * FROM aggregated_regions
