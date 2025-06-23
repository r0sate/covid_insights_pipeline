from agent.pipeline import run_pipeline

def get_response(user_input: str) -> str:
    try:
        result = run_pipeline(user_input)
        return {
            "error": False,
            "response": result
        }
    except Exception as e:
        print(e)
        return {
            "error": True,
            "message": str(e),
            "code": getattr(e, "code", 500)  # se tiver um código, inclui
        }