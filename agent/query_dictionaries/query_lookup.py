from agent.query_dictionaries.query_dictionary import *
from agent.schema_structures.OCRSchema import *
from agent.schema_structures.Schema import ClaimCategory, DocumentCategory

def get_parser_system_query(
        claim_category:ClaimCategory,
        document_category:DocumentCategory) -> str:

    match document_category:
        case DocumentCategory.PRESCRIPTION:
            return get_prescription_system_query(PrescriptionOCR, document_category, claim_category)
        case DocumentCategory.HOSPITAL_BILL:
            return get_hospital_bill_system_query(HospitalBillOCR, document_category, claim_category)
        case DocumentCategory.LAB_REPORT:
            return get_lab_report_system_query(LabReportOCR, document_category, claim_category)
        case DocumentCategory.DIAGNOSTIC_REPORT:
            return get_diagnostic_report_system_query(DiagnosticReportOCR, document_category, claim_category)
        case DocumentCategory.DISCHARGE_SUMMARY:
            return get_discharge_summary_system_query(DischargeSummaryOCR, document_category, claim_category)
        case DocumentCategory.PHARMACY_BILL:
            return get_pharmacy_bill_system_query(PharmacyBillOCR, document_category, claim_category)
        case _:
            return ""

def get_parser_human_query(ocr_text: str) -> str:
    return get_common_human_parser_query(ocr_text)

def get_processor_system_query(
        document_category: DocumentCategory,
        claim_category: ClaimCategory) -> str:

    match document_category:
        case DocumentCategory.PRESCRIPTION:
            return get_prescription_processor_query(claim_category)
        case DocumentCategory.HOSPITAL_BILL:
            return get_hospital_bill_processor_query(claim_category)
        case DocumentCategory.LAB_REPORT:
            return get_lab_report_processor_query(claim_category)
        case DocumentCategory.DIAGNOSTIC_REPORT:
            return get_diagnostic_report_processor_query(claim_category)
        case DocumentCategory.DISCHARGE_SUMMARY:
            return get_discharge_summary_processor_query(claim_category)
        case DocumentCategory.PHARMACY_BILL:
            return get_pharmacy_bill_processor_query(claim_category)
        case _:
            return ""

def get_processor_human_query(user_data, ocr_data) -> str:
    return get_common_processor_human_query(user_data, ocr_data)