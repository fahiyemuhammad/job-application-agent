from langchain_groq import ChatGroq
from tools.skill_matcher import match_skills
from datetime import date

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4)


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

    # Skill matching
    match_results = match_skills(resume_skills, job_skills)
    state["match_results"] = match_results

    matched = match_results["matched_skills"]
    missing = match_results["missing_skills"]
    score = match_results["match_score"]

    # Resolve personal details
    candidate_name = personal_info.get("name") or "the applicant"
    candidate_email = personal_info.get("email") or ""
    candidate_phone = personal_info.get("phone") or ""
    today = date.today().strftime("%B %d, %Y")

    # Try to get company name from scraped title or user input
    company_name = state.get("scraped_job_title", "") or state.get("user_input", "the company")

    prompt = f"""You are a professional career coach writing a cover letter on behalf of a job applicant.

APPLICANT DETAILS (from their resume):
Name: {candidate_name}
Email: {candidate_email}
Phone: {candidate_phone}
Date: {today}

FULL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SKILL MATCH ANALYSIS:
- Matched skills ({score}% match): {", ".join(matched) if matched else "none identified"}
- Skills to address positively: {", ".join(missing[:6]) if missing else "none"}

INSTRUCTIONS:
- Write a complete, professional cover letter addressed to the Hiring Manager
- Use the applicant's REAL name, email, and phone — never use placeholders like [Your Name]
- Fill the company name from context (job description or URL content); if unclear use "your organization"
- In the opening paragraph, show genuine enthusiasm for the specific role/company
- In the body, highlight 2–3 specific achievements or experiences from the resume that are most relevant
- For missing skills, briefly acknowledge eagerness to grow in those areas — do NOT dwell on gaps
- Keep tone confident, warm, and professional
- Length: 3–4 paragraphs, no bullet points inside the letter
- End with a clear call to action
- Output ONLY the cover letter text — no preamble, no "here is your cover letter", no improvement notes
"""

    response = llm.invoke(prompt)
    state["cover_letter"] = response.content.strip()
    return state