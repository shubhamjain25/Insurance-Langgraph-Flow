from typing import TypedDict, Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field
import operator
from enum import Enum
from datetime import date


# ---------------------------------------------------------
# PLUG-IN OCR SCHEMAS
# ---------------------------------------------------------

class ConsultationOCR(BaseModel):
    # This is the discriminator field. It MUST perfectly match the string value
    doc_type: Literal["CONSULTATION"] = Field(description="Must be exactly 'CONSULTATION'")

    patient_name: str = Field(description="Stores the name of the patient")
    doctor_name: str = Field(description="Name of the consulting doctor")
    diagnosis: str = Field(description="The primary diagnosis")
    prescribed_medication: str = Field(description="List of prescribed medicines")
    bill_amt: float = Field(description="Amount charged for the consultation")


class DiagnosticOCR(BaseModel):
    # This is the discriminator field. It MUST perfectly match the string value
    doc_type: Literal["DIAGNOSTIC"] = Field(description="Must be exactly 'DIAGNOSTIC'")

    patient_name: str = Field(description="Stores the name of the patient")
    test_name: str = Field(description="Name of the diagnostic test performed")
    result_readings: str = Field(description="The actual readings/values from the test")
    is_abnormal: bool = Field(description="True if any reading is flagged as abnormal")
    bill_amt: float = Field(description="Amount charged for the diagnostic test")