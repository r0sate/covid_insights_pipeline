import os
from sqlalchemy import create_engine
from typing import List, Optional


def get_engine():

    snowflake_url = (
        f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}@"
        f"{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}/{os.getenv('SNOWFLAKE_SCHEMA')}?role={os.getenv('SNOWFLAKE_ROLE')}"
    )

    print("Snowflake connection string:")
    print(snowflake_url)


    return create_engine(snowflake_url)


def fetch_data(sql: str) -> List[dict]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(sql)
        return [dict(row) for row in result]