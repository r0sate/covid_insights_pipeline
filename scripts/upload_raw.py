
from os import getcwd, path, remove,getenv

from dotenv import load_dotenv

from datetime import date

from typing import Optional

from snowflake.connector import connect
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

import argparse

import pandas as pd

load_dotenv()


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
        user=getenv('SNOWFLAKE_USER'),
        password=getenv('SNOWFLAKE_PASSWORD'),
        account=getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=getenv('SNOWFLAKE_WAREHOUSE'),
        database=getenv('SNOWFLAKE_DATABASE'),
        schema=getenv('SNOWFLAKE_SCHEMA'),
        client_session_keep_alive=False,
        session_parameters={"QUERY_TAG": "debug_dbt_user"}
    )

    cursor: SnowflakeCursor = conn.cursor()

    try:
        if not table_exists(cursor, TABLE_NAME):
            create_table(cursor, TABLE_NAME)
        

        max_date: Optional[date] = get_max_date(cursor, TABLE_NAME)
        # print(max_date)



        parser = argparse.ArgumentParser()
        parser.add_argument("--force-update", action="store_true")
        args = parser.parse_args()


        df: pd.DataFrame = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'], unit='ns').dt.date
        # df.drop_duplicates(subset=["iso_code", "date"], keep="last", inplace=True)
        # df = df[
        #     ~(
        #         df['new_cases'].notna() & df['population'].notna() &
        #         (
        #             ((df['population'] < 10_000) & (df['new_cases'] > df['population'] * 0.30)) |  # until 30% for micro-countries
        #             ((df['population'] < 100_000) & (df['new_cases'] > df['population'] * 0.20)) |  # until 20%
        #             ((df['population'] < 1_000_000) & (df['new_cases'] > df['population'] * 0.10)) |  # until 10%
        #             ((df['population'] < 10_000_000) & (df['new_cases'] > df['population'] * 0.08)) |  # until 7%
        #             ((df['population'] < 100_000_000) & (df['new_cases'] > df['population'] * 0.07)) |  # until 5%
        #             ((df['population'] < 1_000_000_000) & (df['new_cases'] > df['population'] * 0.05)) |  # until 3%
        #             (df['new_cases'] > df['population'] * 0.02)  # above 1 bi: max 2%
        #         )
        #     )
        # ]
        df.reset_index(drop=True, inplace=True)

        
        
        if not args.force_update:
            df: pd.DataFrame = df[df["date"] > max_date] if max_date else df 
        else:
            print("--force-update selected, the tables will be reseted and all rows will be uploaded again...")
            print("Deleting...")
            cursor.execute(f"TRUNCATE TABLE DBT_RAW.{TABLE_NAME}")
            print("Deleted...\nUploading all data again...")

        success, nchunks, nrows, _ = write_pandas(
                    conn=conn,
                    df=df,
                    table_name=TABLE_NAME,
                    database='COVID_DB',
                    schema='DBT_RAW',
                    quote_identifiers=False
                )

        if success:
            print(f"[INFO] {nrows} lines sucessfully inserted via `write_pandas`.")
        else:
            print("[ERROR] Load failed `write_pandas`.")

    
    finally:
 
        conn.close()


if __name__ == "__main__":
    URL_ADDRESS = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    file_path: str = path.join(getcwd(), "tmp", "owid_covid_data.csv")
    

    # Updates with the most recent data provided by Our World in Data
    if fetch_data(URL_ADDRESS, file_path):

        # It loads to Snowflake
       load_raw_data(file_path)

    if path.exists(file_path):
        remove(file_path)