# 📤 COVID-19 Data Uploader (OWID → Snowflake)

This repository contains a Python script to **download COVID-19 data from Our World in Data (OWID)** and **upload it to Snowflake**, preparing it for downstream analytics pipelines (e.g., dbt transformations).

---

## 🌐 Source

- **Data URL:** [Our World in Data – COVID-19 dataset](https://covid.ourworldindata.org/data/owid-covid-data.csv)
- **Format:** CSV
- **Updated:** Daily

---

## 🚀 What This Script Does

- Downloads the most recent `owid-covid-data.csv` file.
- Filters for **new records only**, based on the max date in your Snowflake table.
- Cleans and saves a temporary CSV if needed.
- Uploads new data to a Snowflake table: `COVID_DB.DBT_RAW.OWID_COVID_DATA_RAW`.
- Uses the `write_pandas()` function for efficient loading.

---

## 📁 File Structure

```
.
├── scripts/
│   └── upload_raw.py        ← Main script for download + upload
├── tmp/                     ← Temporary local storage
├── tests/                   ← Custom SQL tests for data quality
│   ├── test_missing_dates_per_country.sql
│   └── test_total_cases_monotonic_or_constant.sql
├── run_pipeline.sh          ← Shell script to automate full pipeline
├── .env                     ← Snowflake credentials (not committed)
├── requirements.txt         ← Python dependencies
└── README.md
```

---

## 🔐 Environment Variables

This project uses environment variables to manage Snowflake credentials.  
Create a `.env` file in the project root:

```env
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=COVID_WH
SNOWFLAKE_DATABASE=COVID_DB
SNOWFLAKE_SCHEMA=DBT_RAW
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

---

## 📦 Installation

Create and activate a virtual environment (recommended), then install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

---

## ⚙️ Usage

To run the ingestion script:

```bash
python scripts/upload_raw.py
```

To run the full pipeline including dbt models and tests:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## ✅ Tests

This project includes SQL-based data quality checks:

- `test_missing_dates_per_country.sql`: checks if each iso_code has full date coverage.
- `test_total_cases_monotonic_or_constant.sql`: flags rows where cumulative cases are stagnant or decrease.

These tests are triggered automatically by `dbt test`.

---

## 🧪 Column-Level Tests with dbt-expectations

This project also uses the [`dbt-expectations`](https://hub.getdbt.com/calogica/dbt_expectations/latest/) package for validating numerical integrity of selected fields:

| Column                  | Rule                                     |
|-------------------------|------------------------------------------|
| `date`                 | Must not be null                         |
| `total_cases`          | Must be strictly greater than 0          |
| `new_cases`            | Must be greater than or equal to 0       |
| `total_deaths`         | Must be greater than or equal to 0       |
| `people_fully_vaccinated` | Must be greater than or equal to 0   |
| `total_tests`          | Must be greater than or equal to 0       |
| `new_vaccinations`     | Must be greater than or equal to 0       |
| `positive_rate`        | Must be between 0 and 1 inclusive        |

These tests are declared in `facts_covid_metrics.yml` and are executed with:

```bash
dbt test
```
---

## 🛠 Dependencies

- `pandas`
- `python-dotenv`
- `snowflake-connector-python[pandas]`

> All specified in `requirements.txt`.

---

## 📦 Optional: Integrate with dbt

Once the data is loaded into `DBT_RAW`, it can be referenced as a source in your dbt project:

```yaml
sources:
  - name: dbt_raw
    database: COVID_DB
    schema: DBT_RAW
    tables:
      - name: owid_covid_data_raw
```

---

## 📫 Contact

For questions or improvements, reach out at: rosate.lucas@gmail.com


---



