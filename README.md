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

Output:

- Confirms if new data was found
- Uploads the delta to Snowflake
- Deletes the temporary file afterward

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
