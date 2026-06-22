from typing import TypedDict, Annotated, Optional, Literal, NotRequired
from pydantic import BaseModel, Field
import operator
from langgraph.graph import add_messages
from enum import Enum
from datetime import date
from agent.schema_structures.OCRSchema import *

class ClaimCategory(str, Enum):
    CONSULTATION = "CONSULTATION"
    DIAGNOSTIC = "DIAGNOSTIC"
    PHARMACY = "PHARMACY"
    DENTAL = "DENTAL"
    VISION = "VISION"
    ALTERNATIVE_MEDICINE = "ALTERNATIVE_MEDICINE"

class DocumentCategory(str, Enum):
    PRESCRIPTION = "PRESCRIPTION"
    HOSPITAL_BILL = "HOSPITAL_BILL"
    LAB_REPORT = "LAB_REPORT"
    DIAGNOSTIC_REPORT = "DIAGNOSTIC_REPORT"
    DISCHARGE_SUMMARY = "DISCHARGE_SUMMARY"
    PHARMACY_BILL = "PHARMACY_BILL"

class UserInputInformation(BaseModel):
    patient_name: str = Field(
        description="Stores the name of the patient"
    )
    treatment_date: date = Field(
        description="Date of the treatment"
    )
    claimed_amt: float = Field(
        description="Amount of the bill"
    )

# Pydantic will check the "doc_type" field & dynamically decide
# which specific OCR Schema to use for validation.
# DYNAMIC UNION (Replaced the old static OCRInformation)
DynamicOCRInformation = Annotated[
    Union[PrescriptionOCR, HospitalBillOCR, LabReportOCR, DiagnosticReportOCR, DischargeSummaryOCR, PharmacyBillOCR],
    Field(discriminator="doc_type")
]

# # Pydantic will check the "doc_type" field & dynamically decide
# # which specific OCR Schema to use for validation.
# DynamicOCRInformation = Annotated[
#     Union[ConsultationOCR, DiagnosticOCR],
#     Field(discriminator="doc_type")

class ProcessingResult(BaseModel):
    result: Literal["PASS", "REVIEW", "FAIL"] = Field(
        description="Final evaluation outcome"
    )
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Model confidence score between 0 and 1"
    )
    reasoning: str = Field(
        description="3-Liner explanation of the decision"
    )

class DocumentValidator(TypedDict):

    user_information : UserInputInformation
    ocr_information: DynamicOCRInformation
    processing_result: ProcessingResult
    status: Literal["initiated","parsed_success","parsed_failure","parse_aborted","parse_rejected","processed"]
    count_itr: Annotated[int, operator.add] = 0
    document_name: str
    claimed_amt: float
    claim_category: ClaimCategory
    document_category: DocumentCategory
