from agent.schema_structures.Schema import *

def aggregator_agent(p_state: DocumentValidator):
    print("+ Entered Aggregator Agent")

    if p_state["status"] == "processed":
        print("+ Passed Aggregator Agent")
        return {
            'status' : 'workflow_completed',
            'count_itr': 1
        }

    else:

        if p_state["status"] == "parsed_success":

            result = ProcessingResult(
                result="FAIL",
                confidence_score=1.0,
                reasoning=f"FAILED: {p_state['ocr_information'].reasoning}"
            )

        else:
            result = ProcessingResult(
                result="FAIL",
                confidence_score=1.0,
                reasoning="Unable to upload & process image via OCR. Might be some network/latency issue. Please try again later."
            )

    print("+ Passed Aggregator Agent")

    return {
        'count_itr':1,
        'processing_result': result,
        'status': 'workflow_completed',
    }