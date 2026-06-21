from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from main import compiled_graph
from agent.schema_structures.Schema import DocumentValidator, ClaimCategory
import os
import shutil
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

# @app.post("/process-claim")
# async def run_langgraph(
#     patient_name: str = Form(default="Kumar Saravana"),
#     claim_category: str = Form(...),
#     treatment_date: str = Form(...),
#     claimed_amt: float = Form(...),
#     document: UploadFile = File(...)
# ):

@app.post("/process-claim")
async def run_langgraph(
    patient_name: str = Form(default="Kumar Saravana"),
    claim_category: ClaimCategory = Form(default="IPD"),
    treatment_date: date = Form(default=date(2014, 1, 11)),
    claimed_amt: float = Form(default="1000"),
    document: UploadFile = File(...)
):
    # Save the uploaded file locally
    file_path = f"uploads/{document.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    # We initialize the status as "initiated" and pass the user details
    initial_state = {
        "user_information": {
            "patient_name": patient_name,
            "claim_category": claim_category,
            "treatment_date": treatment_date,
            "claimed_amt": claimed_amt,
        },
        "document_name": document.filename,
        "status": "initiated",
        "count_itr": 0
    }

    # 3. Run the graph
    # LangGraph will process this and output a state matching your DocumentValidator schema
    final_state: DocumentValidator = compiled_graph.invoke(initial_state)

    # 4. Return the typed schema back to React
    return {"status": "success", "data": final_state}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)