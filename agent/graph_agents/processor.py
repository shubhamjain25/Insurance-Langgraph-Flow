from agent.schema_structures.Schema import *
from agent.llm_models import get_deterministic_llm
from agent.query_dictionaries.query_lookup import get_processor_system_query, get_processor_human_query
from langchain_core.messages import SystemMessage, HumanMessage
import json

def processor_agent(p_state: DocumentValidator):
    print("+ Entered Processor Agent")
    try:

        llm = get_deterministic_llm()

        system_query = str(get_processor_system_query())
        human_query = str(get_processor_human_query(p_state['user_information'], p_state['ocr_information']))

        llm_resp = llm.invoke([
            SystemMessage(content=system_query),
            HumanMessage(content=human_query),
        ])

        # Using this because llm.with_structured_output was throwing error
        # since its open-source model
        data = json.loads(llm_resp.content)
        structured_processing_output = ProcessingResult(**data)

        print("="*20)
        print(structured_processing_output)

    except Exception as e:
        status = "parsed_failure"
        print(e)

    print("+ Passed Processor Agent")
    return {
        'status': "processed",
        'processing_result': structured_processing_output,
        'count_itr':1
    }