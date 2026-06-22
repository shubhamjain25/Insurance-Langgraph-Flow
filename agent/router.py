from agent.schema_structures.Schema import *

def parser_router(p_state: DocumentValidator):
    if p_state["status"] == "parsed_success":
        if p_state["ocr_information"].clarity_score > 0.4 and p_state["ocr_information"].classification_score > 0.4:   #threshold after hit & try
            return "APPROVED"   #Document is of acceptable quality
        else:
            return "REJECTED"   #Document is not of acceptable quality
    elif p_state["status"] == "parsed_failure":
        return "FAILED"         #Unable to parse the document
    else:
        return "RETRY_EXHAUSTED" #Retries exhausted for OCR