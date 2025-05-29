SELECT
  -- Natural key
  iso_code,
  date,

  -- Cases and deaths
  total_cases,
  new_cases,
  total_deaths,
  new_deaths,

  -- Transmission and hospitalization
  reproduction_rate,
  icu_patients,
  hosp_patients,
  weekly_icu_admissions,
  weekly_hosp_admissions,

  -- Testing
  total_tests,
  new_tests,
  positive_rate,

  -- Vaccination
  total_vaccinations,
  people_vaccinated,
  people_fully_vaccinated,
  total_boosters,
  new_vaccinations,

  -- Government response
  stringency_index,

  -- Demographic and socioeconomic indicators
  population,
  population_density,
  median_age,
  aged_65_older,
  aged_70_older,
  gdp_per_capita,
  extreme_poverty,
  female_smokers,
  male_smokers,
  life_expectancy,
  human_development_index

FROM {{ ref('stg_owid_covid_data') }}
WHERE iso_code IS NOT NULL AND date IS NOT NULL
