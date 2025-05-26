SELECT
  -- Natural key
  iso_code,
  date,

  -- Cases and deaths
  total_cases,
  new_cases,
  new_cases_smoothed,
  total_deaths,
  new_deaths,
  new_deaths_smoothed,

  -- Transmission and hospitalization
  reproduction_rate,
  icu_patients,
  hosp_patients,
  weekly_icu_admissions,
  weekly_hosp_admissions,

  -- Testing
  total_tests,
  new_tests,
  new_tests_smoothed,
  positive_rate,
  tests_per_case,

  -- Vaccination
  total_vaccinations,
  people_vaccinated,
  people_fully_vaccinated,
  total_boosters,
  new_vaccinations,
  new_vaccinations_smoothed,
  new_people_vaccinated_smoothed,

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
  cardiovasc_death_rate,
  diabetes_prevalence,
  female_smokers,
  male_smokers,
  handwashing_facilities,
  hospital_beds_per_thousand,
  life_expectancy,
  human_development_index,

  -- Excess mortality
  excess_mortality_cumulative_absolute,
  excess_mortality_cumulative,
  excess_mortality

FROM {{ ref('stg_owid_covid_data') }}
WHERE iso_code IS NOT NULL AND DATE IS NOT NULL
