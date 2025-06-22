import json
import time

from dotenv import load_dotenv
from typing import Optional

from .connector import fetch_data
from .prompts import build_prompt_agent0
from .agent_0_query_builder import call_llm_agent0
from .agent_1_breakdown import call_llm_agent1
from .agent_2_consolidation import call_llm_agent2

from .get_summary import auto_summarize_dataframe


load_dotenv()
    

def run_pipeline(user_question: str) -> Optional[str]:
    
    # AGENT 0 - Query builder
    sql_response = call_llm_agent0(user_question)

    #print(sql_response)

    sql = sql_response.strip().strip("```sql").strip("```").strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Agent 0 didn't return a valid SELECT SQL statement.")
    
    data = fetch_data(sql)

    if not data:
        return "No data was returned for this query."
    
    
    data_summary = auto_summarize_dataframe(data)
    print(f"==========================Response agent 0: ========================================\n{data_summary}")
    
    # AGENT 1 - The Technical Data Analyst
    technical_explanation = call_llm_agent1(user_question, data_summary)
    #print(f"==========================Response agent 1: ========================================\n{technical_explanation}")

    # AGENT 2 - The Storyteller
    final_response = call_llm_agent2(technical_explanation)
    #print(f"==========================Response agent 2: ========================================\n{final_response}")


    return final_response
