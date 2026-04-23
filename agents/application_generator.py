import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.skill_matcher import match_skills
from datetime import date

load_dotenv()

key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key= key, model="llama-3.1-8b-instant", temperature=0.4)


def application_generator(state: dict) -> dict:
    """
    Generates a tailored cover letter using:
    - Full resume text (not just skill list)
    - Matched/missing skills
    - Personal info extracted from resume
    - Job description context
    """
    resume_text = state["resume_text"]
    resume_skills = state["resume_skills"]
    job_skills = state["job_skills"]
    job_description = state["job_description"]
    personal_info = state.get("personal_info", {})

    match_results = match_skills(resume_skills, job_skills)
    state["match_results"] = match_results

    matched = match_results["matched_skills"]
    missing = match_results["missing_skills"]
    score = match_results["match_score"]

    candidate_name = personal_info.get("name") or "the applicant"
    candidate_email = personal_info.get("email") or ""
    candidate_phone = personal_info.get("phone") or ""
    today = date.today().strftime("%B %d, %Y")

    company_name = state.get("scraped_job_title", "") or state.get("user_input", "the company")

    prompt = f"""You are a professional career coach writing a cover letter on behalf of an applicant. Your goal is to highlight the candidate's most relevant skills and experiences for the role, regardless of the industry.

APPLICANT DETAILS:
Name: {candidate_name}
Email: {candidate_email}
Phone: {candidate_phone}
Date: {today}

FULL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SKILL MATCH ANALYSIS:
- Matched competencies ({score}% match): {", ".join(matched) if matched else "none identified"}
- Gaps to bridge: {", ".join(missing[:6]) if missing else "none"}

INSTRUCTIONS:
- Write a professional cover letter that is highly tailored to the specific industry and role.
- GROUNDING: Support EVERY claim with evidence from the FULL RESUME. Do not invent skills or experience.
- EXPERIENCE GUARD: Do NOT calculate or state total years of experience (e.g., "5+ years") unless it is explicitly written on the resume. Stick to specific dates and role durations mentioned.
- If the role is non-technical (e.g. Biomedical, Sales, Education), use the appropriate professional tone and terminology.
- Use the applicant's REAL contact info.
- Fill the company name from context.
- Keep tone confident, warm, and professional.
- Output ONLY the cover letter text.
"""

    response = llm.invoke(prompt)
    state["cover_letter"] = response.content.strip()
    return state