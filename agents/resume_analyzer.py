import os
from dotenv import load_dotenv
import json
from langchain_groq import ChatGroq
from tools.resume_parser import extract_personal_info

load_dotenv()

key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=key, model="llama-3.1-8b-instant", temperature=0)


def resume_analyzer(state: dict) -> dict:
    """
    Extracts:
      - technical and professional skills (industry-agnostic)
      - personal info (name, email, phone)
    """
    resume_text = state["resume_text"]

    personal_info = extract_personal_info(resume_text)
    state["personal_info"] = personal_info

    prompt = f"""You are a high-fidelity resume parser. Your goal is to extract a comprehensive list of professional competencies and skills from the resume text provided.

STRICT GUIDELINES:
1. Extract ONLY skills, tools, and competencies that are explicitly mentioned or clearly evidenced in the resume.
2. DO NOT hallucinate common industry skills (e.g., "Agile", "Docker", "AWS") if they are missing.
3. BE INDUSTRY-AGNOSTIC: Include laboratory techniques, medical technologies, sales methodologies, educational strategies, or any other domain-specific skills.
4. Categories to include: Hard Skills, Soft Skills, Specific Tools/Software, Industry Standards, Certifications, and Languages.

Return ONLY a valid JSON array of strings.
Example: ["Critical Thinking", "Laboratory Research", "Project Management", "Python"]

Resume Text:
---
{resume_text}
---
"""
    response = llm.invoke(prompt)

    try:
        raw = response.content.strip().strip("```json").strip("```").strip()
        skills = json.loads(raw)
    except Exception:
        skills = []

    state["resume_skills"] = [s.strip() for s in skills if isinstance(s, str) and s.strip()]
    return state