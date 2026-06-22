from typing import TypedDict, Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator
import operator
from enum import Enum
from datetime import date

# ---------------------------------------------------------
# PLUG-IN OCR SCHEMAS
# ---------------------------------------------------------
class PrescriptionOCR(BaseModel):
    # This is the discriminator field. It MUST perfectly match the string value
    doc_type: Literal["PRESCRIPTION"] = Field(description="Must be exactly 'PRESCRIPTION'")

    patient_name: str = Field(description="Stores the name of the patient")
    doctor_name: str = Field(description="Name of the diagnostic test performed")
    treatment_date: Optional[date] = Field(default=None, description="Date of prescription")
    diagnosis: str = Field(description="Doctor's comments and/or diagnosis done during prescription")
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )

    #To deal with open-source LLM issues
    @field_validator("patient_name","doctor_name", "diagnosis", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v

class HospitalBillOCR(BaseModel):
    doc_type: Literal["HOSPITAL_BILL"] = Field(
        description="Must be exactly 'HOSPITAL_BILL'"
    )

    patient_name: str = Field(description="Name of the patient")
    hospital_name: str = Field(description="Name of the hospital")
    bill_date: Optional[date] = Field(default=None, description="Date of bill generation")
    total_amount: float = Field(description="Total billed amount", default=0)
    bill_number: str = Field(description="Hospital bill or invoice number")
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )
    #To deal with open-source LLM issues
    @field_validator("patient_name","hospital_name", "bill_number", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v

class LabReportOCR(BaseModel):
    doc_type: Literal["LAB_REPORT"] = Field(
        description="Must be exactly 'LAB_REPORT'"
    )

    patient_name: str = Field(description="Name of the patient")
    test_name: str = Field(description="Primary laboratory test performed")
    report_date: Optional[date] = Field(default=None, description="Date of lab report")
    laboratory_name: str = Field(description="Name of the laboratory")
    result_summary: str = Field(
        description="Key findings, abnormal values, or overall conclusion"
    )
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )

    #To deal with open-source LLM issues
    @field_validator("patient_name","test_name", "laboratory_name","result_summary", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v

class DiagnosticReportOCR(BaseModel):
    doc_type: Literal["DIAGNOSTIC_REPORT"] = Field(
        description="Must be exactly 'DIAGNOSTIC_REPORT'"
    )

    patient_name: str = Field(description="Name of the patient")
    test_name: str = Field(
        description="Diagnostic procedure performed such as X-ray, CT, MRI, ECG"
    )
    report_date: Optional[date] = Field(default=None, description="Date of report generation")
    reporting_doctor: str = Field(
        description="Doctor or radiologist who issued the report"
    )
    impression: str = Field(
        description="Impression, findings, or final conclusion of the report"
    )
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )

    #To deal with open-source LLM issues
    @field_validator("patient_name","reporting_doctor", "impression", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v

class DischargeSummaryOCR(BaseModel):
    doc_type: Literal["DISCHARGE_SUMMARY"] = Field(
        description="Must be exactly 'DISCHARGE_SUMMARY'"
    )

    patient_name: str = Field(description="Name of the patient")
    hospital_name: str = Field(description="Name of the hospital")
    admission_date: Optional[date] = Field(default=None, description="Date of admission")
    discharge_date: Optional[date] = Field(default=None, description="Date of discharge")
    diagnosis: str = Field(
        description="Final diagnosis or reason for hospitalization"
    )
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )

    #To deal with open-source LLM issues
    @field_validator("patient_name","hospital_name", "diagnosis", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v


class PharmacyBillOCR(BaseModel):
    doc_type: Literal["PHARMACY_BILL"] = Field(
        description="Must be exactly 'PHARMACY_BILL'"
    )

    patient_name: str = Field(
        description="Patient name if present on the bill"
    )
    pharmacy_name: str = Field(description="Name of the pharmacy")
    bill_date: Optional[date] = Field(default=None, description="Date of bill generation")
    total_amount: float = Field(description="Total billed amount")
    bill_number: str = Field(description="Pharmacy invoice or receipt number", default=0)
    classification_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the document being correct with respect to claim category & document category. 1 means highly-confident, 0 means incorrect document"
    )
    clarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Ability to make out the text clearly from the photo & parse it. 1 means highly-parsable, 0 means unable to identify any fields"
    )
    reasoning: str = Field(
        description="2-Liner explanation of the clarity_score & classification_score"
    )

    #To deal with open-source LLM issues
    @field_validator("patient_name","pharmacy_name", "bill_number", mode="before")
    @classmethod
    def fix_none_strings(cls, v):
        return "" if v is None else v