from agent.schema_structures.Schema import *

def aggregator_agent(p_state: DocumentValidator):
    print("+ Entered Aggregator Agent")

    if p_state["status"] == "parse_aborted":
        # Exit gracefully
        print("Retries of processing aborted. Unable to process image")
    else:
        # Process successful OCR
        print("Able to process image")

    print("+ Passed Aggregator Agent")

    return {
        'count_itr':1
    }