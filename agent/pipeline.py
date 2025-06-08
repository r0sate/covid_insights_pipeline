import json
from dotenv import load_dotenv
from typing import Optional

from .connector import fetch_data
from .prompts import build_prompt_agent0, build_prompt_agent1, build_prompt_agent2
from .agent_0_query_builder import call_llm_agent0
from .agent_1_breakdown import call_llm_agent1
from .agent_2_consolidation import call_llm_agent2



load_dotenv()
    

def run_pipeline(user_question: str, max_rows: int = 100) -> Optional[str]:
    prompt0 = build_prompt_agent0(user_question)
    sql_response = call_llm_agent0(prompt0)

    sql = sql_response.strip().strip("```sql").strip("```").strip()

    print(sql)

    if not sql.lower().startswith("select"):
        raise ValueError("Agent 0 didn't return a valid SELECT SQL statement.")
    
    data = fetch_data(sql)

    if not data:
        return "No data was returned for this query."

    data_json = json.dumps(data, ident=2)

    prompt1 = build_prompt_agent1(data_json)
    technical_explanation = call_llm_agent1(prompt1)

    prompt2 =  build_prompt_agent2(user_question, technical_explanation)
    final_response = call_llm_agent2(prompt2)

    return final_response
