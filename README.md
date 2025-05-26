# 🧪 COVID Insights Pipeline (dbt + Snowflake)

This project implements a transformation pipeline using **dbt (Data Build Tool)**, structured around public COVID-19 data from [Our World in Data (OWID)](https://ourworldindata.org/coronavirus). The goal is to organize this data into clean, analytics-ready tables following a layered architecture (raw → staging → marts), suitable for BI tools like Power BI and Tableau.

---

## 📁 Project Structure

```
covid_insights_pipeline/
│
├── models/
│   ├── staging/              ← Cleaned raw data (views)
│   └── marts/
│       ├── dimensions/       ← Dimension tables (dim_date, dim_location, etc.)
│       └── facts/            ← Main fact table (fct_covid_metrics)
│
├── seeds/                    ← OWID CSV data
├── macros/                   ← Custom macros (optional)
├── tests/                    ← SQL tests (data quality, logic)
├── dbt_project.yml           ← Main dbt config file
└── README.md
```

---

## 🧩 Components

### 🔹 Seeds
- `owid_covid_data.csv`: downloaded directly from OWID
  - Loaded into the `DBT_RAW` schema
  - Column types defined via `column_types` in `dbt_project.yml`

### 🔹 Staging (`DBT_STAGING`)
- Raw cleanup and casting
- Example: `stg_owid_covid_data.sql`

### 🔹 Dimensions (`DBT_DIM`)
- `dim_location`: countries and regions
- `dim_location_type`: type indicator (country vs. aggregate)
- `dim_date`: calendar table for time-based joins

### 🔹 Facts (`DBT_FACT`)
- `fct_covid_metrics`: daily metrics per country

---

## ✅ Data Quality Tests

Includes:
- Standard `dbt` tests: `not_null`, `unique`, `relationships`
- Custom logic with [dbt-expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/)
- Custom SQL tests:
  - `test_missing_dates_per_country.sql`
  - `test_total_cases_monotonic.sql`

---

## 🚀 How to Run

1. Install dependencies

```
dbt deps
```

2. Fetch the OWID dataset

```
python fetch_data.py
```

Or with Makefile (if available):

```
make fetch
```

3. Load the seed data

```
dbt seed
```

4. Build all models

```
dbt run
```

5. Run data quality tests

```
dbt test
```

6. (Optional) Generate and view documentation

```
dbt docs generate
dbt docs serve
```

---

## 🐚 Optional: Shell Script for Full Pipeline Execution

If you prefer running the full dbt pipeline via a shell script, you can use the provided `run_pipeline.sh` file:

```bash
#!/bin/bash
set -e  # Exit on first error

echo "🔽 Fetching latest COVID-19 data from OWID..."
python fetch_data.py

echo "🌱 Seeding data into your warehouse..."
dbt seed

echo "🏗️ Running dbt models..."
dbt run

echo "✅ Running dbt tests..."
dbt test

echo "📘 Generating documentation..."
dbt docs generate

echo "✨ Done!"
```

### 📦 How to use:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

This will sequentially execute:  
1. Data fetch from OWID  
2. Seeding into Snowflake  
3. Model builds  
4. Data quality tests  
5. Documentation generation  

Make sure your virtual environment or dbt environment is activated before running the script.

---

## 🏗️ Snowflake Structure

| Layer      | Schema         | Description                          |
|------------|----------------|--------------------------------------|
| Raw        | DBT_RAW        | Seed data (OWID)                     |
| Staging    | DBT_STAGING    | Views with cleaned, typed columns    |
| Dimensions | DBT_DIM        | Lookup/dimension tables              |
| Facts      | DBT_FACT       | Fact table with COVID-19 metrics     |

---

## 🔐 Permissions (Example)

```sql
GRANT USAGE ON DATABASE COVID_DB TO ROLE MASTER_ROLE;
GRANT USAGE ON WAREHOUSE COVID_WH TO ROLE MASTER_ROLE;

GRANT USAGE ON SCHEMA COVID_DB.DBT_RAW TO ROLE MASTER_ROLE;
GRANT USAGE ON SCHEMA COVID_DB.DBT_STAGING TO ROLE MASTER_ROLE;
GRANT USAGE ON SCHEMA COVID_DB.DBT_DIM TO ROLE MASTER_ROLE;
GRANT USAGE ON SCHEMA COVID_DB.DBT_FACT TO ROLE MASTER_ROLE;

GRANT SELECT ON FUTURE TABLES IN SCHEMA COVID_DB.DBT_FACT TO ROLE MASTER_ROLE;
GRANT ROLE MASTER_ROLE TO USER covid_user_access;
```

---

## 🛠 Requirements

- Python 3.8+
- dbt >= 1.6
- Snowflake account with appropriate roles
- dbt packages:
  - `dbt-utils`
  - `dbt-expectations`

---

## 📌 Notes

- All models must reside in proper subfolders (`staging/`, `marts/`) or dbt will raise schema errors
- Use a neutral `schema: dbt` in `profiles.yml` to avoid automatic schema name concatenation
- The project uses naming conventions like `DBT_RAW`, `DBT_STAGING`, etc. for clarity

---

## 📫 Contact

E-mail me: rosate.lucas@gmail.com


## 🛡️ License

This project is intended for educational and analytical purposes. The data may be subject to updates and structural changes from the original source.