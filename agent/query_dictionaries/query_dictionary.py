from agent.schema_structures.Schema import *
from pydantic import BaseModel

# COMMON_INSTRUCTIONS = """
#
# CRITICAL INSTRUCTIONS:
# 1. You must output the ACTUAL DATA extracted from the text.
# 2. DO NOT output the schema definitions or 'properties' blocks.
# 3. DO NOT wrap the output in markdown code blocks (like ```json). Just return the raw JSON braces.
#
# Instructions:
# - Use only information explicitly present in the OCR text.
# - If information is blurry or unclear give a lower clarity_score.
# - If information does not align with the claim & document category, give a lower confidence_score.
# - If numeric fields are unknown, return 0. Do not return null.
# - If a field cannot be determined, return null/0/blank depending on its type.
# - Do not invent, infer, or hallucinate values.
# """

COMMON_INSTRUCTIONS = """

CRITICAL INSTRUCTIONS:
1. You must output the ACTUAL DATA extracted from the text.
2. DO NOT output the schema definitions or 'properties' blocks.
3. DO NOT wrap the output in markdown code blocks (like ```json). Just return the raw JSON braces.

IMPORTANT CONTEXT: You are NOT looking at the original photo. You only see OCR-extracted
text, which is a downstream artifact of that photo. You cannot directly judge blur — you
can only infer document quality from how complete and coherent the OCR text is. Treat the
OCR text as your only evidence of image quality.

CLARITY_SCORE RUBRIC (you must follow this exactly — it is not a vague impression):
- Start clarity_score at 1.0, then deduct for each issue found in the OCR text:
  - Deduct 0.15 for EVERY required schema field that is null, blank, or "0" because it
    could not be located in the OCR text (a field missing because the document genuinely
    doesn't have it — e.g. no bill_date printed — counts the same as a field obscured by
    blur; you cannot distinguish the two from text alone, so both must lower the score).
  - Deduct 0.1 for every field whose value looks fragmented, truncated, or contains
    OCR noise (random symbols, broken words, inconsistent spacing, repeated characters).
  - Deduct 0.1 if multiple words in the OCR text appear malformed or nonsensical, even
    in fields you are not extracting (this signals general scan/photo quality).
  - Deduct 0.2 if the OCR text is extremely short or sparse relative to what this
    document type should normally contain.
- Floor clarity_score at 0.0. Do not round up to compensate for a "mostly readable" feel.

CONSISTENCY RULE (mandatory):
- If your reasoning states that ANY field "could not be identified," "is unclear,"
  "is missing," or similar — clarity_score MUST be 0.75 or lower. A reasoning that
  admits missing information paired with a clarity_score above 0.75 is a contradiction
  and is not allowed.
- Re-read your own reasoning before finalizing clarity_score and check this rule.

General Instructions:
- Use only information explicitly present in the OCR text.
- classification_score reflects whether the document's CONTENT (not its clarity) matches
  the declared claim_category and document_category. Keep this independent of clarity_score.
- If numeric fields are unknown, return 0. Do not return null.
- If string fields are unknown, return empty string "". Do not return null.
- If a non-numeric field cannot be determined, return null/blank depending on its type.
- Do not invent, infer, or hallucinate values.
- In `reasoning`, explicitly name every field that was missing, blank, or low quality —
  do not just describe the document generally.
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

# ---------------------------------------------------------
# PROCESSOR COMMON RULES (shared across all doc types)
# ---------------------------------------------------------

PROCESSOR_COMMON_INSTRUCTIONS = f"""
CRITICAL OUTPUT INSTRUCTIONS:
1. DO NOT wrap output in markdown code blocks. Return raw JSON only.
2. Do not invent, infer, or hallucinate values.
3. Return strictly in the format {ProcessingResult.model_json_schema()} — no metadata, no extra fields.

Decision Thresholds:
- PASS   → confidence_score >= 0.75 AND all applicable rules below pass
- REVIEW → confidence_score >= 0.5 and < 0.75
- FAIL   → any hard rule fails OR confidence_score < 0.5

Confidence Score:
- Range: 0.0 to 1.0
- Higher when all fields strongly match with no ambiguity
- Lower when OCR errors, partial matches, or missing fields exist

Reasoning:
- Exactly TWO lines:
  Line 1: What was compared and what matched or mismatched
  Line 2: Why the final decision was reached
"""


# ---------------------------------------------------------
# NON-FINANCIAL PROCESSOR QUERIES
# (PRESCRIPTION, LAB_REPORT, DIAGNOSTIC_REPORT, DISCHARGE_SUMMARY)
# No total_amount field exists in these OCR schemas.
# Financial comparison must NOT be performed.
# ---------------------------------------------------------

def get_prescription_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a PRESCRIPTION document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - doctor_name
        - treatment_date
        - diagnosis

        ---------------------------
        Reconciliation Rules:

        1. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        2. Date Match:
           - OCR treatment_date must match user-provided treatment_date
           - Allow format differences (DD-MM-YYYY vs YYYY-MM-DD etc.)
           - If OCR treatment_date is null/missing, penalise confidence but do not auto-FAIL

        3. Document Relevance:
           - Diagnosis and prescription content must be plausibly relevant to the {claim_category} claim
           - A prescription for dental work under a CONSULTATION claim is acceptable
           - An irrelevant or mismatched diagnosis should lower confidence

        4. NO financial comparison — this document type carries no billed amount.

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


def get_lab_report_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a LAB_REPORT document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - test_name
        - report_date
        - laboratory_name
        - result_summary

        ---------------------------
        Reconciliation Rules:

        1. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        2. Date Match:
           - OCR report_date must match or be close to user-provided treatment_date
           - Lab reports may be dated 1–3 days before or after treatment; allow this window
           - If OCR report_date is null/missing, penalise confidence but do not auto-FAIL

        3. Document Relevance:
           - test_name and result_summary must be plausibly relevant to the {claim_category} claim
           - A blood test under a CONSULTATION claim is acceptable
           - Completely unrelated tests should lower confidence

        4. NO financial comparison — this document type carries no billed amount.

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


def get_diagnostic_report_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a DIAGNOSTIC_REPORT document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - test_name
        - report_date
        - reporting_doctor
        - impression

        ---------------------------
        Reconciliation Rules:

        1. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        2. Date Match:
           - OCR report_date must match or be close to user-provided treatment_date
           - Diagnostic reports may be dated 1–3 days before or after treatment; allow this window
           - If OCR report_date is null/missing, penalise confidence but do not auto-FAIL

        3. Document Relevance:
           - test_name (e.g. X-Ray, MRI, CT, ECG) and impression must be plausibly relevant to the {claim_category} claim
           - Completely unrelated procedures should lower confidence

        4. NO financial comparison — this document type carries no billed amount.

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


def get_discharge_summary_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a DISCHARGE_SUMMARY document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - hospital_name
        - admission_date
        - discharge_date
        - diagnosis

        ---------------------------
        Reconciliation Rules:

        1. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        2. Date Window Check:
           - User-provided treatment_date must fall within the OCR admission_date to discharge_date window (inclusive)
           - If either admission_date or discharge_date is null/missing, penalise confidence but do not auto-FAIL
           - treatment_date falling outside the window is a hard FAIL

        3. Document Relevance:
           - diagnosis must be plausibly relevant to the {claim_category} claim
           - Unrelated diagnoses should lower confidence

        4. NO financial comparison — this document type carries no billed amount.

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


# ---------------------------------------------------------
# FINANCIAL PROCESSOR QUERIES
# (HOSPITAL_BILL, PHARMACY_BILL)
# These OCR schemas contain total_amount — financial check applies.
# ---------------------------------------------------------

def get_hospital_bill_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a HOSPITAL_BILL document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claimed_amount
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - hospital_name
        - bill_date
        - total_amount
        - bill_number

        ---------------------------
        Reconciliation Rules:

        1. Financial Rule:
           - If OCR total_amount >= claimed_amount → financial check passes
           - If OCR total_amount < claimed_amount → financial check fails (hard FAIL)
           - If OCR total_amount is 0 or missing → penalise confidence heavily but do not auto-FAIL

        2. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        3. Date Match:
           - OCR bill_date must match user-provided treatment_date
           - Allow format differences (DD-MM-YYYY vs YYYY-MM-DD etc.)
           - If OCR bill_date is null/missing, penalise confidence but do not auto-FAIL

        4. Final Decision:
           PASS only if ALL three rules pass and confidence_score >= 0.75
           REVIEW if confidence_score >= 0.5 and < 0.75
           FAIL if financial rule fails OR confidence_score < 0.5

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


def get_pharmacy_bill_processor_query(claim_category) -> str:
    return f"""
        You are an expert medical-claim reconciliation engine evaluating a PHARMACY_BILL document
        submitted under a {claim_category} claim.

        You compare two inputs:

        Input 1 (User Claim Data):
        - patient_name
        - treatment_date
        - claimed_amount
        - claim_category

        Input 2 (OCR Extracted Data):
        - patient_name
        - pharmacy_name
        - bill_date
        - total_amount
        - bill_number

        ---------------------------
        Reconciliation Rules:

        1. Financial Rule:
           - If OCR total_amount >= claimed_amount → financial check passes
           - If OCR total_amount < claimed_amount → financial check fails (hard FAIL)
           - If OCR total_amount is 0 or missing → penalise confidence heavily but do not auto-FAIL

        2. Patient Name Match:
           - Names must match (allow minor OCR spelling variations and abbreviations)

        3. Date Match:
           - OCR bill_date must match user-provided treatment_date
           - Allow format differences (DD-MM-YYYY vs YYYY-MM-DD etc.)
           - Pharmacy bills may be dated 1–2 days after the treatment date; allow this window
           - If OCR bill_date is null/missing, penalise confidence but do not auto-FAIL

        4. Final Decision:
           PASS only if ALL three rules pass and confidence_score >= 0.75
           REVIEW if confidence_score >= 0.5 and < 0.75
           FAIL if financial rule fails OR confidence_score < 0.5

        {PROCESSOR_COMMON_INSTRUCTIONS}
    """


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