
from openai import OpenAI
from sqlglot import parse_one, errors as sqlglot_errors
import os
import re
from typing import Optional


from .prompts import build_prompt_agent0







VALID_COLUMNS = {
    "date", "location", "iso_code",
    "new_cases", "total_cases",
    "new_deaths", "total_deaths",
    "population"
}


def fix_sql_syntax(sql: str) -> Optional[str]:
    try:
        # print("\n\nraw:"+sql)
        parsed = parse_one(sql, dialect="snowflake")
        # print("\n\nparsed:"+ parsed.sql(dialect="snowflake"))
        return parsed.sql(dialect="snowflake")

    except sqlglot_errors.ParseError:
        return None

def has_invalid_columns(sql: str) -> bool:

    cleaned_query = re.sub(r"\s+AS\s+\b\w+\b", sql, "", flags=re.IGNORECASE)
    matches = re.findall(r"\b[a-zA-Z]+\b", cleaned_query)
    columns_used = set(matches)

    potential_columns = columns_used - {
        "SELECT", "FROM", "WHERE", "AND", "OR", "BY", "LIMIT", "ORDER", "AS", "OVER", "PARTITION", "BETWEEN",
        "CURRENT_DATE", "LAG", "SUM", "AVG", "ROUND", "DESC", "ASC", "ON", "JOIN", "ROWS", "PRECEDING", "CAST", "FLOAT"
    }

    return any(col.lower() not in VALID_COLUMNS for col in potential_columns)



def call_llm_agent0(question: str) -> str:
    prompt: str = build_prompt_agent0(question)

    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    model = os.getenv("OPENAI_MODEL")
    messages = [
            {
                "role": "system",
                "content": (
                    "You are agent0, a strict SQL generator for Snowflake.\n"
                    "Your job is to return only a valid SQL query in response — no explanations, no preambles, no formatting. "
                    "Your answers must be silent and direct: exactly one SQL SELECT statement, and nothing else."
                )
            },
            {
                 "role": "user",
                 "content": prompt
            }
        ]


    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    sql = response.choices[0].message.content.strip()

    if has_invalid_columns(sql):
        print("Invalid columns, resending the response to the model...")

        messages.append(
            {
                "role": "assistant",
                "content": sql
            }
        )

        messages.append(
            {
                "role": "user",
                "content": "Please, check your SQL: you are using invalid columns or using as reference invalid aliases. Retry only using valid fields"
            }
        )

        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
    
        if has_invalid_columns(sql):
            raise ValueError("After a second retry, generated SQL contains invalid columns.")
        
    sql_fixed = fix_sql_syntax(sql)

    if not sql_fixed:
        raise ValueError("Failed to transform semantically correct.")
    

    return sql_fixed
