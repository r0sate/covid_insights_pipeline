import json
from dotenv import load_dotenv
from typing import Optional

from .connector import fetch_data
from .prompts import build_prompt_agent0, build_prompt_agent1, build_prompt_agent2
from .agent_0_query_builder import call_llm_agent0
from .agent_1_breakdown import call_llm_agent1
from .agent_2_consolidation import call_llm_agent2



load_dotenv()
    

def run_pipeline(user_question: str) -> Optional[str]:
    
    # AGENT 0 - Query builder
    prompt0 = build_prompt_agent0(user_question)
    sql_response = call_llm_agent0(prompt0)

    sql = sql_response.strip().strip("```sql").strip("```").strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Agent 0 didn't return a valid SELECT SQL statement.")
    
    data = fetch_data(sql)

    print(sql)

    if not data:
        return "No data was returned for this query."

    data_json = json.dumps(data, indent=2)

    # AGENT 1 - The Technical Data Analyst
    technical_explanation = call_llm_agent1(user_question, data_json)

    # AGENT 2 - The Storyteller
    final_response = call_llm_agent2(technical_explanation)

    return final_response
