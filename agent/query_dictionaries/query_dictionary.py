from agent.schema_structures.Schema import *
from pydantic import BaseModel

COMMON_INSTRUCTIONS = """

CRITICAL INSTRUCTIONS:
1. You must output the ACTUAL DATA extracted from the text.
2. DO NOT output the schema definitions or 'properties' blocks. 
3. DO NOT wrap the output in markdown code blocks (like ```json). Just return the raw JSON braces.

Instructions:
- Use only information explicitly present in the OCR text.
- If information is blurry or unclear give a lower clarity_score.
- If information does not align with the claim & document category, give a lower confidence_score.
- If numeric fields are unknown, return 0. Do not return null.
- If a field cannot be determined, return null/0/blank depending on its type.
- Do not invent, infer, or hallucinate values.
"""


def get_prescription_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a prescription document and extract all information and return it strictly as a JSON object

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract prescribing doctor details if available.
        - Extract prescribed medicines, dosage, frequency, duration, and instructions.
        - Normalize medicine names only when clearly identifiable from OCR text.
        - Extract prescription date if present.
        - Capture registration/license numbers exactly as written.
        - Handle handwritten or partially recognized OCR content carefully and reflect uncertainty through clarity_score.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
    """


def get_hospital_bill_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a hospital bill and extract all information and return it strictly as a JSON object.

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract hospital details, patient details, invoice numbers, admission/discharge dates, and billing dates.
        - Normalize currency amounts when possible.
        - Extract itemized charges, taxes, discounts, and total payable amounts.
        - Preserve monetary values exactly as represented if normalization is not possible.
        - Extract payment mode and receipt references if available.
        - Handle duplicate line items caused by OCR errors carefully.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
        """


def get_lab_report_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a laboratory report and extract all information and return it strictly as a JSON object.

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract patient details, laboratory details, sample collection dates, report dates, and report identifiers.
        - Extract test names, test results, units, reference ranges, and abnormality indicators.
        - Preserve values exactly as reported.
        - Do not interpret medical significance beyond what is explicitly stated.
        - Extract laboratory comments and observations if present.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
        """


def get_diagnostic_report_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a diagnostic report and extract all information and return it strictly as a JSON object.

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract patient details, diagnostic center details, report identifiers, and report dates.
        - Extract diagnostic procedure names (e.g. X-Ray, MRI, CT, Ultrasound) exactly as written.
        - Extract findings, impressions, conclusions, and observations.
        - Preserve medical terminology exactly as reported.
        - Do not infer diagnoses that are not explicitly stated.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
        """


def get_discharge_summary_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a discharge summary and extract all information and return it strictly as a JSON object.

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract hospital details, patient details, admission date, discharge date, and length of stay if explicitly stated.
        - Extract diagnoses, procedures, treatments, and discharge condition.
        - Extract treating doctor details and discharge instructions.
        - Extract follow-up recommendations and prescribed medications if present.
        - Preserve medical terminology exactly as reported.
        - Do not infer diagnoses, procedures, or outcomes not explicitly documented.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
        """


def get_pharmacy_bill_system_query(
        relevant_schema: type[BaseModel],
        document_category,
        claim_category,
) -> str:
    return f"""
        You are an insurance document parser.

        Your task is to analyze OCR-extracted text from a pharmacy bill and extract all information and return it strictly as a JSON object.

        Claim Category: {claim_category}
        Document Category: {document_category}

        {COMMON_INSTRUCTIONS}

        Additional Instructions:
        - Extract pharmacy details, invoice numbers, invoice dates, and payment information.
        - Extract medicine names, quantities, unit prices, discounts, taxes, and total amounts.
        - Normalize currency amounts when possible.
        - Preserve medicine names exactly as printed when OCR confidence is low.
        - Handle duplicate or fragmented OCR entries carefully.
        - Extract prescription references if present.

        Return strictly in the format {relevant_schema.model_json_schema()} and do not provide any metadata or any other information other than the schema.
        """


def get_common_human_parser_query(ocr_text: str) -> str:
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

def get_common_processor_system_query() -> str:
    query = f"""
        You are an expert medical-claim reconciliation engine. You compare two inputs
        
        Input 1 (User Claim Data):
        - claimed_amount
        - patient_name
        - treatment_date
        - claim_category
        
        Input 2 (OCR Extracted Data):
        - patient_name
        - bill_amount
        - treatment_date
        - claim_category
        - document_category     
        ---------------------------
        Instructions:
        
        1. Financial Rule:
        - If bill_amount >= claimed_amount → PASS
        - If bill_amount < claimed_amount → FAIL
        
        2. Field Matching:
        - patient_name must match (allow minor OCR spelling variations)
        - treatment_date must match exactly (format differences allowed)
        
        3. Final Decision:
        PASS only if ALL are true and confidence score>=0.75:
        - Financial rule passes
        - Patient name matches
        - Treatment date matches
        
        REVIEW if confidence score>=0.5 and <0.75:
        
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


def get_common_processor_human_query(user_data, ocr_data) -> str:
    query = f"""
        Compare the following two inputs and return the evaluation in the required JSON format.
        
        Input 1 (User Claim Data): {user_data}
        
        Input 2 (OCR Extracted Data): {ocr_data}        
    """
    return query

# def get_parser_system_query() -> str:
#     query = f"""
#         You are an insurance document parser.
#
#         Your task is to analyze OCR-extracted text from insurance-related documents and extract all information and return it strictly as a JSON object.
#
#         Instructions:
#         - Use only information explicitly present in the OCR text.
#         - Normalize dates, currency amounts, phone numbers, and identifiers when possible.
#         - If a field cannot be determined, return null.
#         - Do not invent, infer, or hallucinate values.
#         - Extract information even if the OCR text contains formatting errors, spelling mistakes, broken lines, or duplicated content.
#         - If multiple values exist for the same field, choose the most relevant value and include any ambiguity in the notes field if available.
#         - Return strictly in the format{OCRInformation.model_json_schema()} and do not provide any metadata or any other information other than the schema.
#     """
#     return query
#
# def get_parser_human_query(ocr_text: str) -> str:
#     query = f"""
#         The following is raw OCR text extracted from an insurance-related document.
#
#         Analyze the text and populate the structured output schema with all relevant information you can identify.
#
#         OCR Text:
#         --------------------
#         {ocr_text}
#         --------------------
#
#         Extract all available information and return the result in the required structured format.
#     """
#     return query