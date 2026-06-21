from typing import TypedDict, Annotated, Optional, Literal, NotRequired
from pydantic import BaseModel, Field
import operator
from langgraph.graph import add_messages
from enum import Enum
from datetime import date

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
    claim_category: ClaimCategory = Field(
        description="Category of the uploaded document"
    )
    treatment_date: date = Field(
        description="Date of the treatment"
    )
    claimed_amt: float = Field(
        description="Amount of the bill"
    )

class OCRInformation(BaseModel):
    patient_name: str = Field(
        description="Stores the name of the patient"
    )
    claim_category: ClaimCategory = Field(
        description="Category of the uploaded document"
    )
    treatment_date: date = Field(
        description="Date of the treatment"
    )
    bill_amt: float = Field(
        description="Amount of the bill"
    )

# # Pydantic will check the "doc_type" field & dynamically decide
# # which specific OCR Schema to use for validation.
# DynamicOCRInformation = Annotated[
#     Union[ConsultationOCR, DiagnosticOCR],
#     Field(discriminator="doc_type")

class ProcessingResult(BaseModel):
    result: Literal["PASS", "FAIL"] = Field(
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
    ocr_information: OCRInformation
    processing_result: ProcessingResult
    status: Literal["initiated","parsed_success","parsed_failure","parse_aborted","processed"]
    count_itr: Annotated[int, operator.add] = 0
    document_name: str
    claim_category: ClaimCategory
    claimed_amt: float
