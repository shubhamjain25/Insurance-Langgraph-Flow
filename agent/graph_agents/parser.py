from agent.schema_structures.Schema import *
from agent.image_processor import extract_text, extract_text_hardcoded
from agent.llm_models import get_deterministic_llm
from agent.query_dictionaries.query_lookup import get_parser_system_query, get_parser_human_query
from langchain_core.messages import SystemMessage, HumanMessage
import json
from pydantic import TypeAdapter
import re

def parser_agent(p_state: DocumentValidator):
    print("+ Entered Parser Agent")
    img_text = ""
    status = "parsed_failure"   #Default as failure

    document_name = p_state["document_name"]

    result = extract_text(document_name)
    # result = extract_text_hardcoded() # Swapped while testing to curb api-burnonout

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

            system_query = str(get_parser_system_query(p_state['claim_category'], p_state['document_category'] ))
            human_query = str(get_parser_human_query(img_text))

            llm_resp = llm.invoke([
                SystemMessage(content=system_query),
                HumanMessage(content=human_query),
            ])

            #Using this because llm.with_structured_output was throwing error
            #since its open-source model
            # data = json.loads(llm_resp.content)
            # structured_ocr_output = DynamicOCRInformation(**data)

            #This is also throwing error, need to hardcode it.
            # raw_content = llm_resp.content
            # print("="*20)
            # print(raw_content)
            # print("=" * 20)
            # # Safety Net: Strip out markdown formatting if the model accidentally adds it
            # raw_content = raw_content.replace("```json", "").replace("```", "").strip()
            # # Safety Net: Find the first '{' and the last '}' in case of conversational fluff
            # json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            # if not json_match:
            #     raise ValueError("The LLM did not return any JSON.")
            # clean_json_string = json_match.group(0)
            # # Now it is safe to load and adapt
            # data = json.loads(clean_json_string)
            # ocr_adapter = TypeAdapter(DynamicOCRInformation)
            # structured_ocr_output = ocr_adapter.validate_python(data)

            #hardcoded because it was throwing errors since we are using an open source model
            #with lower compatibilities
            data = json.loads(llm_resp.content)

            match p_state["document_category"]:
                case DocumentCategory.PRESCRIPTION:
                    structured_ocr_output = PrescriptionOCR(**data)
                case DocumentCategory.HOSPITAL_BILL:
                    structured_ocr_output = HospitalBillOCR(**data)
                case DocumentCategory.LAB_REPORT:
                    structured_ocr_output = LabReportOCR(**data)
                case DocumentCategory.DIAGNOSTIC_REPORT:
                    structured_ocr_output = DiagnosticReportOCR(**data)
                case DocumentCategory.DISCHARGE_SUMMARY:
                    structured_ocr_output = DischargeSummaryOCR(**data)
                case DocumentCategory.PHARMACY_BILL:
                    structured_ocr_output = PharmacyBillOCR(**data)
                case _:
                    raise Exception(f"Unknown Document Category: {p_state['document_category']}")


            print("+ Passed Parser Agent")
            return {
                'status': status,
                'count_itr': 1,
                'ocr_information': structured_ocr_output
            }

        except Exception as e:
            status = "parsed_failure"
            print(e)


    if status == "parsed_failure" and p_state["count_itr"]>=3 :
        #Short Circuiting after 2 retries to avoid-infinite loops
        status = "parse_aborted"

    print(status)
    print("+ Passed Parser Agent")
    return {
        'status':status,
        'count_itr':1,
    }