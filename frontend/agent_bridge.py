from agent.pipeline import run_pipeline

def get_response(user_input: str) -> str:
    try:
        return run_pipeline(user_input)
    except Exception as e:
        return f"Ocorreu um erro ao processar a pergunta: {str(e)}"
