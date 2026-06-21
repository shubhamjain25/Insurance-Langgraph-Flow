import requests
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

OCRSPACE_API_KEY = os.getenv("OCRSPACE_API_KEY")

def extract_text(document_name):

    file_path = Path(__file__).parent.parent / "uploads" / document_name

    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://api.ocr.space/parse/image",
                files={"file": f},
                headers={"apikey": OCRSPACE_API_KEY},
                data={
                    "OCREngine": 3,
                    "language": "auto",
                    "detectOrientation": True,
                    "scale": True
                }
            )

        response.raise_for_status()
        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return {
                "success": False,
                "error": result.get("ErrorMessage"),
                "text": None,
            }

        text = "\n".join(
            page.get("ParsedText", "")
            for page in result.get("ParsedResults", [])
        )

        return {
            "success": True,
            "error": None,
            "text": text.strip(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": None,
        }


def extract_text_hardcoded():
    hardcoded_text_val = f"""
        ====================
        # Apollo
        ## APOLLO HOSPITALS
        EMERGENCY 1066
        Opposite IIMB, 154/11, Amalodbhavi Nagar, Panduranga Nagar,
        Bangalore-560076 (India)
        HOSPITALS Tel.: +(91)-80-26304050/26304051 Fax: +(91)-80-41463151
        TOUCHING LIVES

        ### INPATIENT BILL
        | PATIENT DETAILS | | IP No. : 97101 | ID No.: 0000246611 |
        |---|---|---|---|
        | Saravana kumar V | | Bill No.: ICR33504 | |
        | A2 Nagesan nagar | | Bill Dt./Time: 13-Jan-2013 10:06 AM | |
        | Vadalur | | Admission Dt./Time: 10-Jan-2014 7:22 AM | |
        | Cuddalore taluk | | Discahrge Dt./Time: 13-Jan-2014 10:06 AM | |
        | TamilNadu | | | |

        ## DETAILS
        | Service Name | Amount (Rs.) |
        |---|---|
        | ROOM RENT | 4,000.00 |
        | PHARMACY | 2,765.54 |
        | MEDICAL EQUIPMENT | 1,000.00 |
        | CONSULTATIONS | 2,400.00 |
        | CONSUMABLES | 2,118.00 |
        | INVESTIGATIONS | 2,860.00 |

        Bill Amount 15,143.54

        In Words:
        Fifteen Thousand Hundred Forty Three Rupees and Fifty Four Paise

        Refundable Deposit As On 13-Jan-2014 10:05 AM Rs.5000

        This is a computer generated statement and requires no signature.
        This Receipt is valid foran employer or insurer, who is contractually obligated to reimburse the medicalexpenses covered by Medisave
        and/or MediShield.
        For billing and generalenquiries, please mail: customercare_bangalore@apollohospitals.com
        © Apollo Hospitals, Bangalore 2013, All Rights reserved
    """

    return {
        "success": True,
        "error": None,
        "text": hardcoded_text_val.strip(),
    }