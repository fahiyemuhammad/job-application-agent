"""
FastAPI backend for the ApplyAI job application assistant.

Run with:
    uvicorn api:app --reload --port 8000

Install extra deps (once):
    pip install fastapi uvicorn python-multipart --break-system-packages
"""

import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from tools.resume_parser import parse_resume
from graph.agent_workflow import build_graph

app = FastAPI(title="ApplyAI API", version="1.0.0")

# Allow the Vite dev server (port 5173) and any production origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(..., description="PDF résumé"),
    job_input: str = Form(..., description="Job URL, company name, or pasted description"),
):
    # ── Validate file type ──
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF résumés are supported.")

    # ── Save upload to a temp file ──
    try:
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await resume.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save résumé: {e}")

    # ── Parse résumé ──
    try:
        resume_text = parse_resume(tmp_path)
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(status_code=422, detail=f"Could not read PDF: {e}")
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if not resume_text.strip():
        raise HTTPException(status_code=422, detail="The PDF appears to be empty or image-only.")

    # ── Build initial state ──
    state = {
        "resume_text": resume_text,
        "user_input": job_input.strip(),
        "input_type": "",
        "job_description": "",
        "scraped_job_title": "",
        "personal_info": {},
        "resume_skills": [],
        "job_skills": [],
        "match_results": {},
        "cover_letter": "",
        "improved_cover_letter": "",
    }

    # ── Run agent graph ──
    try:
        graph = build_graph()
        result = graph.invoke(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent pipeline error: {e}")

    # ── Return structured response ──
    return JSONResponse({
        "match_results": result.get("match_results", {}),
        "resume_skills": result.get("resume_skills", []),
        "job_skills": result.get("job_skills", []),
        "job_description": result.get("job_description", ""),
        "cover_letter": result.get("cover_letter", ""),
        "improved_cover_letter": result.get("improved_cover_letter", ""),
        "personal_info": result.get("personal_info", {}),
    })
