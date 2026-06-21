from agent.schema_structures.Schema import *

def get_parser_system_query() -> str:
    query = f"""
        You are an insurance document parser.
    
        Your task is to analyze OCR-extracted text from insurance-related documents and extract all information that can be mapped to the provided structured output schema.
    
        Instructions:
        - Use only information explicitly present in the OCR text.
        - Normalize dates, currency amounts, phone numbers, and identifiers when possible.
        - If a field cannot be determined, return null.
        - Do not invent, infer, or hallucinate values.
        - Extract information even if the OCR text contains formatting errors, spelling mistakes, broken lines, or duplicated content.
        - If multiple values exist for the same field, choose the most relevant value and include any ambiguity in the notes field if available.
        - Return strictly in the format{OCRInformation.model_json_schema()} and do not provide any metadata or any other information other than the schema.
    """
    return query

def get_parser_human_query(ocr_text: str) -> str:
    query = f"""
        The following is raw OCR text extracted from an insurance-related document.
        
        Analyze the text and populate the structured output schema with all relevant information you can identify.
        
        OCR Text:
        --------------------
        {ocr_text}
        --------------------
        
        Extract all available information and return the result in the required structured format.
    """
    return query


def get_processor_system_query() -> str:
    query = f"""
        You are an expert medical-claim reconciliation engine. You compare two inputs
        
        Input 1 (User Claim Data):
        - claimed_amount
        - claim_category
        - patient_name
        - treatment_date
        
        Input 2 (OCR Extracted Data):
        - clean_category
        - patient_name
        - bill_amount
        - treatment_date
        
        ---------------------------
        Instructions:
        
        1. Financial Rule:
        - If bill_amount >= claimed_amount → PASS
        - If bill_amount < claimed_amount → FAIL
        
        2. Field Matching:
        - patient_name must match (allow minor OCR spelling variations)
        - claim_category and clean_category must be semantically similar
        - treatment_date must match exactly (format differences allowed)
        
        3. Final Decision:
        PASS only if ALL are true:
        - Financial rule passes
        - Patient name matches
        - Category matches or is equivalent
        - Treatment date matches
        
        Otherwise FAIL.
        
        4. Confidence Score:
        - Range: 0.0 to 1.0
        - Higher when all fields strongly match
        - Lower when OCR ambiguity, mismatches, or uncertainty exists
        
        5. Explanation:
        - Exactly TWO lines only:
          Line 1: What was compared and matched/mismatched
          Line 2: Why final decision was reached
        
        ---------------------------

        - Do not invent, infer, or hallucinate values.
        - Return strictly in the format{ProcessingResult.model_json_schema()} and do not provide any metadata or any other information other than the schema.
    """
    return query


def get_processor_human_query(user_data, ocr_data) -> str:
    query = f"""
        Compare the following two inputs and return the evaluation in the required JSON format.
        
        Input 1 (User Claim Data): {user_data}
        
        Input 2 (OCR Extracted Data): {ocr_data}        
    """
    return query