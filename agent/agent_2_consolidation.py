import os

from openai import OpenAI
from .prompts import build_prompt_agent2

def call_llm_agent2(agent1_response: str) -> str:
    prompt = build_prompt_agent2(agent1_response)
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are a presenter and a data storyteller."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()