from agent.schema_structures.Schema import *
from agent.image_processor import extract_text
from agent.llm_models import get_deterministic_llm
from agent.query_dictionaries.query_dictionary import get_parser_system_query, get_parser_human_query
from langchain_core.messages import SystemMessage, HumanMessage
import json

def parser_agent(p_state: DocumentValidator):
    print("+ Entered Parser Agent")
    img_text = ""
    status = "parsed_failure"   #Default as failure

    document_name = p_state["document_name"]

    result = extract_text(document_name)
    # result = extract_text_hardcoded("./assets/apollo_bill.jpg") "Swapped while testing to curb api-burnonout

    if result["success"]:
        img_text = result["text"]
        # print("="*20)
        # print(img_text)
        # print("="*20)
        status = "parsed_success"

    else:
        print("OCR failed:", result["error"])

    if status == "parsed_success" and img_text != "":
        try:

            llm = get_deterministic_llm()

            system_query = str(get_parser_system_query())
            human_query = str(get_parser_human_query(img_text))

            llm_resp = llm.invoke([
                SystemMessage(content=system_query),
                HumanMessage(content=human_query),
            ])

            #Using this because llm.with_structured_output was throwing error
            #since its open-source model
            data = json.loads(llm_resp.content)
            structured_ocr_output = OCRInformation(**data)

            print("+ Passed Parser Agent")
            return {
                'status': status,
                'count_itr': 1,
                'ocr_information': structured_ocr_output
            }

        except Exception as e:
            status = "parsed_failure"
            print(e)


    if status == "parsed_failure" and p_state["count_itr"]>=1 :
        #Short Circuiting after 3 retries to avoid-infinite loops
        status = "parse_aborted"

    print(status)
    print("+ Passed Parser Agent")
    return {
        'status':status,
        'count_itr':1,
    }