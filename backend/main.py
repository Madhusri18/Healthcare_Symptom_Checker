from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal, SymptomRecord, init_db

# Initialize FastAPI app
app = FastAPI()

# Initialize DB tables
init_db()



app = FastAPI(
    title="AI Symptom Checker Backend",
    description="FastAPI service using Gemini API to analyze user symptoms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = "AIzaSyD6oYd6BsrGBB_EDU75Ut6qC3MRP7m_zYY"
MODEL_NAME = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"


@app.get("/")
def root():
    return {"message": "AI Symptom Checker Backend is running!"}


def clean_and_format_text(text: str) -> str:
    """Clean and format Gemini output."""
    if not text:
        return "No response text found."

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    lines = text.strip().splitlines()
    cleaned_lines = []
    num = 1

    for line in lines:
        line = line.strip()
        if not line:
            cleaned_lines.append("")
            continue

        if re.search(r"(?i)possible conditions|next steps|disclaimer", line):
            cleaned_lines.append(f"**{line.strip(':')}**")
            num = 1
            continue

        if re.match(r"^[*\-]\s*", line):
            cleaned_lines.append(f"{num}. {re.sub(r'^[*\-]\s*', '', line)}")
            num += 1
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


@app.post("/analyze")
async def analyze_symptoms(request: Request):
    data = await request.json()
    symptoms = data.get("symptoms", "").strip()

    if not symptoms:
        return {"error": "Please provide some symptoms to analyze."}
    
    prompt = f"""
You are an AI healthcare assistant.

The user reports: {symptoms}.

Your task:
Generate a structured, concise, and educational summary analyzing the symptoms.

Formatting rules:
1. Divide the response into three main sections titled:
   - Possible Conditions
   - Next Steps
2. Do NOT use markdown symbols such as **, *, or underscores (_).
3. Use clear numbered lists (1., 2., 3.) and short, crisp sentences.
4. For subsections (like Self-Care Measures, When to See a Doctor, When to Seek Immediate Medical Attention), write their titles in Title Case and end them with a colon.
5. Keep descriptions short (1-2 sentences maximum) for readability.
6. Avoid long paragraphs - make the response easy to scan.


"""


    body = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=body,
            timeout=90
        )

        if response.status_code != 200:
            return {"error": "Failed to get a valid response from Gemini API", "details": response.text}

        data = response.json()
        text_output = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        formatted_output = clean_and_format_text(text_output)
        #  Save analysis and symptoms to database
        db = SessionLocal()
        record = SymptomRecord(symptoms=symptoms, analysis=formatted_output)
        db.add(record)
        db.commit()
        db.close()

        return {"analysis": formatted_output}

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(SymptomRecord).all()
    db.close()
    return [{"id": r.id, "symptoms": r.symptoms, "analysis": r.analysis} for r in records]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
