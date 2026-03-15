import json
from langchain_groq import ChatGroq
from tools.resume_parser import extract_personal_info

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)


def resume_analyzer(state: dict) -> dict:
    """
    Extracts:
      - technical skills (as a JSON list)
      - personal info (name, email, phone) for cover letter
    """
    resume_text = state["resume_text"]

    personal_info = extract_personal_info(resume_text)
    state["personal_info"] = personal_info

    prompt = f"""You are a resume parser. Extract ALL technical and professional skills from the resume below.

Include: programming languages, frameworks, tools, platforms, methodologies, soft skills relevant to tech roles.
Normalize skill names (e.g. "MS Azure" → "Microsoft Azure", "AWS" → "Amazon Web Services (AWS)").

Return ONLY a valid JSON array of strings. No explanation, no markdown, no extra text.

Example output: ["Python", "Django", "REST APIs", "Docker", "Agile"]

Resume:
{resume_text}
"""
    response = llm.invoke(prompt)

    try:
        raw = response.content.strip().strip("```json").strip("```").strip()
        skills = json.loads(raw)
    except Exception:
        skills = []

    state["resume_skills"] = [s.strip() for s in skills if isinstance(s, str) and s.strip()]
    return state