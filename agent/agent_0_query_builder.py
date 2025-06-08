import os
from openai import OpenAI
from .prompts import build_prompt_agent0

def call_llm_agent0(question: str) -> str:
    prompt: str = build_prompt_agent0(question)

    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You generate SQL queries for Snowflake."
            },
            {
                 "role": "user",
                 "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()