from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parser import extract_text_from_pdf
from ai import extract_candidate_info, ask_candidate, generate_evaluation
from agent import create_hr_form
from pdf_service import create_hr_pdf

# FastAPI application exposing the resume, Q&A, evaluation, and PDF workflow.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "HireFlow AI backend is running!"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Task 1:Extract text from the uploaded resume and convert it into structured candidate data.
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    resume_text = extract_text_from_pdf(file_path)
    candidate_info = extract_candidate_info(resume_text)

    return {
        "filename": file.filename,
        "candidate": candidate_info
    }


class AskRequest(BaseModel):
    question: str
    candidate: dict


@app.post("/ask")
def ask(request: AskRequest):

    # Task 2: Answer recruiter questions using only the extracted candidate information.
    answer = ask_candidate(
        request.question,
        request.candidate
    )

    return {
        "question": request.question,
        "answer": answer
    }

class EvaluateRequest(BaseModel):
    candidate: dict


@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    # Generate a structured AI evaluation from the extracted candidate data.
    evaluation = generate_evaluation(request.candidate)

    return {
        "evaluation": evaluation
    }

class HRFormRequest(BaseModel):
    candidate: dict
    evaluation: dict


@app.post("/create-hr-form")
def create_hr_form_endpoint(request: HRFormRequest):
    # Task 3: Automatically map candidate information into the corporate HR evaluation form.
    form = create_hr_form(
        request.candidate,
        request.evaluation
    )

    return {
        "hr_form": form
    }

@app.post("/generate-pdf")
def generate_pdf(request: HRFormRequest):
    # Convert the completed HR evaluation into a downloadable PDF.
    form = create_hr_form(
        request.candidate,
        request.evaluation
    )

    output_path = "candidate_evaluation.pdf"
    # Generate the final HR report that can be downloaded by the recruiter.
    create_hr_pdf(form, output_path)

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename="candidate_evaluation.pdf"
    )