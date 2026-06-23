# 🏥 Claim Wizard — Document Intelligence Pipeline

An AI-powered insurance claim document processing backend built with **LangGraph**, **FastAPI**, and **Groq**. Upload a medical document, and the pipeline automatically performs OCR, field extraction, confidence scoring, and a final PASS/FAIL verdict — all orchestrated as a stateful LangGraph workflow.

- 🎥 [YouTube Architecture & Project Walkthrough](https://www.youtube.com/watch?v=qGBj17hSVvU)
- 🌐 [LangGraph Workflow Live Demo](https://insurance-langgraph-flow.onrender.com/)

---

## 🧠 How It Works

```
__start__
    │
    ▼
input_node              → Validates & structures user inputs into the DocumentValidator state
    │
    ▼
parser_node  ◄──────────────────────────────────────────────┐
    │                                                       │
    │   OCR + LLM extraction into typed schema              │
    │   (PrescriptionOCR, HospitalBillOCR, etc.)            │
    │                                                       │
    ├── APPROVED ──→ processor_node                         │
    │                    │  Final PASS/REVIEW/FAIL          │
                            reasoning with confidence_score │
    │                    │                                  │  
    ├── REJECTED ────────┤                                  │
    │                    │                                  │      FAILED + count_itr < 3
    └── FAILED  ─────────┼──────────────────────────────────┘
         (retry loop,    │
          max 2 retries) │  FAILED + count_itr == 3
                         │  (RETRY_EXHAUSTED)
                         ▼
                  aggregator_node     → Consolidates result into final state
                         │
                         ▼
                      __end__
```

### Routing Logic (`parser_router`)

After `parser_node`, the graph routes based on:

| Condition                                                                             | Route |
|---------------------------------------------------------------------------------------|---|
| `status == parsed_success` AND `clarity_score > 0.4` AND `classification_score > 0.4` | `APPROVED` → `processor_node` |
| `status == parsed_success` but scores below threshold                                 | `REJECTED` → `aggregator_node` |
| `status == parsed_failure` AND `count_itr < 3`                                        | `FAILED` → back to `parser_node` (retry) |
| `status == parsed_failure` AND `count_itr == 3`                                       | `RETRY_EXHAUSTED` → `aggregator_node` |

---

## 📄 Supported Document Types

The pipeline accepts any combination of the following:

**Claim Categories**
`CONSULTATION` · `DIAGNOSTIC` · `PHARMACY` · `DENTAL` · `VISION` · `ALTERNATIVE_MEDICINE`

**Document Categories**
`PRESCRIPTION` · `HOSPITAL_BILL` · `LAB_REPORT` · `DIAGNOSTIC_REPORT` · `DISCHARGE_SUMMARY` · `PHARMACY_BILL`

Each document category maps to a dedicated typed OCR schema (e.g. `PrescriptionOCR`, `HospitalBillOCR`) with two scoring dimensions:

- **`clarity_score`** — How legible/parseable the uploaded image is (`0.0`–`1.0`)
- **`classification_score`** — Confidence that the document matches the declared claim + document category (`0.0`–`1.0`)

---

## 🗂️ Project Structure

```
.
├── api.py                          # FastAPI entry point
├── main.py                         # LangGraph compiled_graph definition
├── requirements.txt
├── .env
├── uploads/                        # Temporarily stores uploaded documents
└── agent/
    ├── graph_agents/
    │   ├── input.py
    │   ├── parser.py
    │   ├── processor.py
    │   └── aggregator.py
    ├── router.py                   # parser_router conditional edge logic
    ├── llm_models.py               # stores the information of models & calling logic
    ├── document_ocr_processor.py   # does the ocr of the uploaded document
    ├── router.py                   # parser_router conditional edge logic
    ├── graph_main.py               # instantiates & stores the graph nodes & edges
    └── schema_structures/
    │   ├── Schema.py               # DocumentValidator TypedDict + Pydantic models
    │   └── OCRSchema.py            # Per-document OCR schemas (PrescriptionOCR, etc.)
    │
    ├── query-dictionaries/
        ├── query_lookup.py.py      # Abstracts the query fetching logic
        ├── query-dictionary.py     # Stores the actual system & human queries to be passed to LLM
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/shubhamjain25/Insurance-Langgraph-Flow.git
cd Insurance-Langgraph-Flow
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key"

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT="your_project_name"

OCRSPACE_API_KEY="your_ocrspace_api_key"

# Hashed key used to authenticate requests to the /process-claim endpoint
API_KEY="your_hashed_api_key"
```

> **Note:** Every request to `/process-claim` must include the header `x-api-key: <API_KEY>`. Requests without a valid key will receive a `401 Unauthorized` response.

---

## 🚀 Running the Server

```bash
python api.py
```

The API will be available at: `http://localhost:8000`

Interactive API docs (Swagger UI): `http://localhost:8000/docs`

---

## 📡 API Reference

### `POST /process-claim`

Accepts a multipart form submission with the document image and claim metadata.

**Headers**

| Header | Value |
|---|---|
| `x-api-key` | Your configured `API_KEY` |

**Form Fields**

| Field | Type | Description |
|---|---|---|
| `patient_name` | `string` | Full name of the patient |
| `treatment_date` | `string` | Date of treatment (`YYYY-MM-DD`) |
| `claimed_amt` | `float` | Amount being claimed |
| `claim_category` | `enum` | One of the supported claim categories |
| `document_category` | `enum` | One of the supported document categories |
| `document` | `file` | The document image to process |

**Example — cURL**

```bash
curl -X POST http://localhost:8000/process-claim \
  -H "x-api-key: your_api_key" \
  -F "patient_name=Kumar Saravana" \
  -F "treatment_date=2024-11-15" \
  -F "claimed_amt=1500.00" \
  -F "claim_category=CONSULTATION" \
  -F "document_category=PRESCRIPTION" \
  -F "document=@/path/to/prescription.jpg"
```

**Response**

```json
{
  "status": "success",
  "data": {
    "status": "processed",
    "ocr_information": {
      "doc_type": "PRESCRIPTION",
      "patient_name": "Kumar Saravana",
      "doctor_name": "Dr. Anita Rao",
      "treatment_date": "2024-11-15",
      "diagnosis": "Acute pharyngitis",
      "clarity_score": 0.87,
      "classification_score": 0.92,
      "reasoning": "Document is clearly legible with all fields identifiable. Strongly matches a CONSULTATION / PRESCRIPTION combination."
    },
    "processing_result": {
      "result": "PASS",
      "confidence_score": 0.91,
      "reasoning": "Patient name, date, and diagnosis are consistent with the claim. Claimed amount is within expected range for a consultation."
    },
    "claim_category": "CONSULTATION",
    "document_category": "PRESCRIPTION"
  }
}
```

---

## 🔍 LangSmith Tracing

When `LANGSMITH_TRACING=true`, every graph invocation is traced end-to-end — including node inputs/outputs, LLM calls, token usage, and latency — visible in your [LangSmith dashboard](https://smith.langchain.com).

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Stateful multi-node agent orchestration |
| `langchain` | LLM abstraction & prompt management |
| `langchain-groq` | Groq LLM integration |
| `fastapi` | REST API server |
| `uvicorn` | ASGI server |
| `pydantic` | Schema validation & typed OCR outputs |
| `python-multipart` | Multipart form / file upload support |

---

## 📝 License

MIT
