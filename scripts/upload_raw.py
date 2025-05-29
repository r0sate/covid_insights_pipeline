
from os import getcwd, path, remove, environ
from datetime import date

from typing import Optional

from snowflake.connector import connect
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

import pandas as pd



# Function developed in order to download and save the .csv file into the destined folder path
def fetch_data(url_address: str, file_path: str)-> bool:
    try:
        df: pd.DataFrame = pd.read_csv(url_address)

        if df.empty:
                print("Error: .csv file is empty.")
                return False

    except Exception as e:
        print(f"Error: Failed to process data: {e}.")

    else:        
        df.to_csv(file_path, index=False)
        print(f"The data was sucessfully saved in the following path: {file_path}.")
        return True
    
    finally:
        print("...")




def table_exists(cursor: SnowflakeCursor, table_name: str)-> bool:
     
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name.upper()}'
        AND TABLE_SCHEMA = 'DBT_RAW'
    """)
    
    return cursor.fetchone()[0] == 1


# Returns the maximum date from date field (if table exists, else returns None)     
def get_max_date(cursor: SnowflakeCursor, table_name: str) -> Optional[date]:
    return cursor.execute(f"SELECT MAX(date) FROM {table_name}").fetchone()[0]

# Create or replace table if exists
def create_table(cursor: SnowflakeCursor, table_name: str):

    
    # Table considering some columns from the .csv
    create_table_sql = f"""
    CREATE OR REPLACE TABLE {table_name} (
        iso_code STRING,
        continent STRING,
        location STRING,
        date DATE,
        total_cases FLOAT,
        new_cases FLOAT,
        new_cases_smoothed FLOAT,
        total_deaths FLOAT,
        new_deaths FLOAT,
        new_deaths_smoothed FLOAT,
        total_cases_per_million FLOAT,
        new_cases_per_million FLOAT,
        new_cases_smoothed_per_million FLOAT,
        total_deaths_per_million FLOAT,
        new_deaths_per_million FLOAT,
        new_deaths_smoothed_per_million FLOAT,
        reproduction_rate FLOAT,
        icu_patients FLOAT,
        icu_patients_per_million FLOAT,
        hosp_patients FLOAT,
        hosp_patients_per_million FLOAT,
        weekly_icu_admissions FLOAT,
        weekly_icu_admissions_per_million FLOAT,
        weekly_hosp_admissions FLOAT,
        weekly_hosp_admissions_per_million FLOAT,
        total_tests FLOAT,
        new_tests FLOAT,
        total_tests_per_thousand FLOAT,
        new_tests_per_thousand FLOAT,
        new_tests_smoothed FLOAT,
        new_tests_smoothed_per_thousand FLOAT,
        positive_rate FLOAT,
        tests_per_case FLOAT,
        tests_units STRING,
        total_vaccinations FLOAT,
        people_vaccinated FLOAT,
        people_fully_vaccinated FLOAT,
        total_boosters FLOAT,
        new_vaccinations FLOAT,
        new_vaccinations_smoothed FLOAT,
        total_vaccinations_per_hundred FLOAT,
        people_vaccinated_per_hundred FLOAT,
        people_fully_vaccinated_per_hundred FLOAT,
        total_boosters_per_hundred FLOAT,
        new_vaccinations_smoothed_per_million FLOAT,
        new_people_vaccinated_smoothed FLOAT,
        new_people_vaccinated_smoothed_per_hundred FLOAT,
        stringency_index FLOAT,
        population_density FLOAT,
        median_age FLOAT,
        aged_65_older FLOAT,
        aged_70_older FLOAT,
        gdp_per_capita FLOAT,
        extreme_poverty FLOAT,
        cardiovasc_death_rate FLOAT,
        diabetes_prevalence FLOAT,
        female_smokers FLOAT,
        male_smokers FLOAT,
        handwashing_facilities FLOAT,
        hospital_beds_per_thousand FLOAT,
        life_expectancy FLOAT,
        human_development_index FLOAT,
        population FLOAT,
        excess_mortality_cumulative_absolute FLOAT,
        excess_mortality_cumulative FLOAT,
        excess_mortality FLOAT,
        excess_mortality_cumulative_per_million FLOAT
    );
    """
    cursor.execute(create_table_sql)




# Load to the table
def load_raw_data(file_path: str):
    TABLE_NAME = "OWID_COVID_DATA_RAW"

    # Connections settings
    conn = connect(
        user=environ['SNOWFLAKE_USER'],
        password=environ['SNOWFLAKE_PASSWORD'],
        account=environ['SNOWFLAKE_ACCOUNT'],
        warehouse=environ['SNOWFLAKE_WAREHOUSE'],
        database=environ['SNOWFLAKE_DATABASE'],
        schema=environ['SNOWFLAKE_SCHEMA'],
        client_session_keep_alive=False,
        session_parameters={"QUERY_TAG": "debug_dbt_user"}
    )

    cursor: SnowflakeCursor = conn.cursor()


    tmp_file_path: str = file_path[:-4] + "_tmp.csv"

    try:
        if not table_exists(cursor, TABLE_NAME):
            create_table(cursor, TABLE_NAME)
        

        max_date: Optional[date] = get_max_date(cursor, TABLE_NAME)
        # print(max_date)

        df: pd.DataFrame = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'], unit='ns').dt.date

        filtered_df: pd.DataFrame = df[df["date"] > max_date] if max_date else df 

       

        filtered_df.to_csv(tmp_file_path, index=False)
        
        cursor.execute(f"PUT file://{tmp_file_path} @%{TABLE_NAME} AUTO_COMPRESS=TRUE")
        cursor.execute(f"LIST @%{TABLE_NAME}")
        # print(cursor.fetchall())

        success, nchunks, nrows, _ = write_pandas(
                    conn=conn,
                    df=filtered_df,
                    table_name=TABLE_NAME,
                    database='COVID_DB',
                    schema='DBT_RAW',
                    quote_identifiers=False
                )

        if success:
            print(f"[INFO] {nrows} linhas inseridas com sucesso via `write_pandas`.")
        else:
            print("[ERROR] Falha no carregamento via `write_pandas`.")

    
    finally:
        if path.exists(tmp_file_path):
            remove(tmp_file_path)
        conn.close()


if __name__ == "__main__":
    URL_ADDRESS = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    file_path: str = path.join(getcwd(), "tmp", "owid_covid_data.csv")

    # if fetch_data(URL_ADDRESS, file_path):
    load_raw_data(file_path)