import os
from urllib.parse import quote
from sqlalchemy import create_engine, text
from typing import List


def get_engine():

    snowflake_url = (
        f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{quote(os.getenv('SNOWFLAKE_PASSWORD'))}@"
        f"{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}/{os.getenv('SNOWFLAKE_SCHEMA')}?role={os.getenv('SNOWFLAKE_ROLE')}"
    )

    return create_engine(snowflake_url)


def fetch_data(sql: str) -> List[dict]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

        return [dict(zip(columns, row)) for row in rows]