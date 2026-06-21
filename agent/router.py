from agent.schema_structures.Schema import *

def parser_router(p_state: DocumentValidator):
    if p_state["status"] == "parsed_success":
        return "APPROVED"
    elif p_state["status"] == "parsed_failure":
        return "FAILED"
    else:
        return "RETRY_EXHAUSTED"