# 🧠 COVID Insights Pipeline with AI Agents and Power BI Integration

This repository automates the ingestion, transformation, and analysis of COVID-19 data from Our World in Data (OWID), enriched with AI-powered analytics and integrated into Power BI via WebSocket.

---

## 🌐 Source

- **Source:** [OWID COVID-19 Dataset](https://covid.ourworldindata.org/data/owid-covid-data.csv)
- **Format:** CSV
- **Update Frequency:** Daily

---

## 🚀 What This Pipeline Does

## 🖼️ Visual Overview

### 📊 Power BI Dashboard

![Power BI Dashboard](https://i.imgur.com/PqnX2eN.gif)

### 💬 WebSocket Interface

![WebSocket Interface](https://i.imgur.com/vRyQ1Zn.png)


This project automates the ingestion and transformation of COVID-19 data through three core components:

### 1. Python Ingestion Script (`upload_raw.py`)
- Downloads the latest COVID-19 dataset from OWID.
- Filters only new records based on max date in Snowflake.
- Uploads to `COVID_DB.DBT_RAW.OWID_COVID_DATA_RAW` via `write_pandas()`.

### 2. dbt Transformations
- **Staging Layer (`DBT.STAGING`)**: Cleans and formats raw data.
- **Mart Layer (`DBT.MART`)**: Builds `facts_covid_metrics`, `dim_date`, and `dim_location`.

### 3.  Power BI + AI Interaction (Independent Applications)

- **Power BI Visual:** An interactive dashboard built in Power BI that consumes transformed data from Snowflake to analyze COVID-19 metrics.
- **Web-based Frontend (Flask + WebSocket):** A separate web application that allows users to input natural language questions.
- **AI Agent Orchestration:**
  - The frontend sends user prompts via WebSocket to a Flask backend.
  - The Flask server queries the data and routes the prompt to 3 AI agents.
  - A consolidated response is returned and displayed in real time in the web interface.
- **Note:** Power BI and the Flask/WebSocket app are **independent applications**, but both consume the **same data from Snowflake**.


#### Agents:
- **Agent 1 (Factual):** Fetches metrics from Snowflake.
- **Agent 2 (Insight):** Interprets and contextualizes trends.
- **Agent 3 (Summarizer):** Crafts final answer for users.

#### Power BI Visual:
- Web-based frontend (HTML/JS or Deneb visual)
- User input → AI agents → Real-time answers rendered

---

## 📁 File Structure

```
.
├── agent/                        ← LLM Agent definitions
├── analyses/
├── dbt_packages/
├── debug.log
├── frontend/
│   ├── static/
│   └── templates/
│       └── index.html           ← WebSocket interface
├── utils/
│   ├── serialize.py
│   ├── agent_bridge.py
│   └── app.py                   ← Flask WebSocket server
├── logs/
├── macros/
├── models/
│   ├── marts/
│   │   ├── dimensions/
│   │   │   ├── dim_dates.sql
│   │   │   ├── dim_locations.sql
│   │   │   └── dim_locations_types.sql
│   │   └── facts/
│   │       ├── facts_covid_metrics.sql
│   │       └── facts_covid_metrics_schema.yml
│   └── staging/
├── scripts/
│   └── upload_raw.py
├── run_pipeline.sh
├── requirements.txt
├── .env
└── README.md
```

---

## 🔐 Environment Variables (.env)

```env
# Snowflake credentials
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=COVID_WH
SNOWFLAKE_DATABASE=COVID_DB
SNOWFLAKE_SCHEMA=DBT_RAW

# AI Agent config
OPENAI_MODEL=[paste_the_model_you_would_like_here]
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=your_api_key
```

> ⚠️ Never commit `.env` to version control.

---

## 📦 Installation

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

---

## ⚙️ Usage

To run ingestion only:
```bash
python scripts/upload_raw.py
```

To run the full pipeline including dbt transformations:
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## ✅ Tests

Includes data quality tests via SQL and dbt:

- `test_missing_dates_per_country.sql`
- `test_total_cases_monotonic_or_constant.sql`

Also includes column-level expectations via `dbt-expectations`:

| Column                     | Rule                            |
|----------------------------|---------------------------------|
| `date`                     | Not null                        |
| `total_cases`              | > 0                             |
| `new_cases`                | ≥ 0                             |
| `total_deaths`             | ≥ 0                             |
| `new_vaccinations`         | ≥ 0                             |
| `positive_rate`            | Between 0 and 1 inclusive       |

Run tests with:

```bash
dbt test
```

---

## 📫 Contact

📧 rosate.lucas@gmail.com
