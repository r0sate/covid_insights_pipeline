import os
from openai import OpenAI
from .prompts import build_prompt_agent1

def call_llm_agent1(user_question: str, data_json: str) -> str:
    prompt = build_prompt_agent1(user_question, data_json)

    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.getenv("OPENROUTER_API_KEY"))
    response = client.chat.completions.create(

        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are a technical data analyst"
            
            },
            {
                "role": "user",
                "role": "user", "content": prompt
            }    
        ]
    )

    return response.choices[0].message.content.strip()