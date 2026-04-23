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
      - technical skills (as a JSON list)
      - personal info (name, email, phone) for cover letter
    """
    resume_text = state["resume_text"]

    personal_info = extract_personal_info(resume_text)
    state["personal_info"] = personal_info

    prompt = f"""You are a high-fidelity resume parser. Your goal is to extract a comprehensive list of technical and professional skills from the resume text provided.

STRICT GUIDELINES:
1. Extract ONLY skills that are explicitly mentioned or clearly evidenced in the resume.
2. DO NOT include common industry skills (like "Agile", "Docker", "REST APIs", "AWS") unless they are actually in the text.
3. Include: programming languages, software tools, frameworks, technical platforms, and industry-specific certifications.
4. Normalize name variations (e.g., "Javascript" to "JavaScript").

Return ONLY a valid JSON array of strings.
Example: ["Skill A", "Skill B", "Skill C"]

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