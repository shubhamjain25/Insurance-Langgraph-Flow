from agent.schema_structures.Schema import *

def parser_router(p_state: DocumentValidator):
    if p_state["status"] == "parsed_success":
        if p_state["ocr_information"].clarity_score > 0.4 and p_state["ocr_information"].classification_score > 0.4:   #threshold after hit & try
            return "APPROVED"
        else:
            return "REJECTED"
    elif p_state["status"] == "parsed_failure":
        return "FAILED"
    else:
        return "RETRY_EXHAUSTED"