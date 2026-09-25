import os
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_candidate_info(resume_text):
    prompt = f"""
You are a recruitment assistant.

Extract candidate information from the resume below.

Return ONLY valid JSON with these fields:
{{
    "name": "",
    "email": "",
    "phone": "",
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "certifications": []
}}

Rules:
- Use ONLY information explicitly present in the resume.
- Do not invent or assume information.
- If information is missing, use an empty string or empty list.
- Keep the extracted information concise.

RESUME:
{resume_text}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            break

        except Exception as e:
            if attempt == 2:
                raise e

            time.sleep(2)

    return response.text

def ask_candidate(question, candidate_data):
    prompt = f"""
You are a recruitment assistant.

Answer the recruiter's question using ONLY the candidate information provided below.

Candidate information:
{candidate_data}

Recruiter question:
{question}

Rules:
- Use only the information provided.
- Do not invent or assume anything.
- If the answer is not present, say:
  "This information is not available in the resume."
- Keep the answer concise and factual.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text

def generate_evaluation(candidate_data):
    prompt = f"""
You are an HR recruitment assistant.

Create a candidate evaluation using ONLY the candidate information provided below.

Candidate information:
{candidate_data}

Return ONLY valid JSON with these fields:

{{
    "candidate_name": "",
    "education": "",
    "experience_summary": "",
    "technical_skills": [],
    "projects": [],
    "strengths": [],
    "missing_information": [],
    "overall_summary": ""
}}

Rules:
- Use ONLY information present in the candidate data.
- Do not invent or assume information.
- If something is missing, clearly mention it in "missing_information".
- Keep the evaluation factual and concise.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text