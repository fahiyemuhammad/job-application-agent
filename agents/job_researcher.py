import os
import json
from langchain_groq import ChatGroq
from tools.job_scraper import scrape_job_posting
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=key, model="llama-3.1-8b-instant", temperature=0)

FALLBACK_DESCRIPTION = (
    "A professional role requiring relevant industry experience, problem-solving, "
    "and strong communication skills aligned with the company's mission."
)


def _extract_skills_from_text(description: str) -> list:
    """Ask LLM to extract & normalize job skills from a description."""
    prompt = f"""You are a job requirements parser. Extract the most important technical and professional skills required for this role from the description below.

STRICT GUIDELINES:
1. Extract ONLY specific skills, tools, or certifications that are listed as requirements or preferences.
2. DO NOT add generic tech buzzwords if they are not present.
3. Normalize variations (e.g. "K8s" to "Kubernetes").

Return ONLY a valid JSON array of strings.

Job Description:
{description}
"""
    response = llm.invoke(prompt)
    try:
        raw = response.content.strip().strip("```json").strip("```").strip()
        skills = json.loads(raw)
    except Exception:
        skills = []
    return [s.strip() for s in skills if isinstance(s, str) and s.strip()]


def job_researcher(state: dict) -> dict:
    """
    Resolves user input into a job description and extracts required skills.
    Infers the role based on candidate background if only a company is provided.
    """
    input_type = state["input_type"]
    user_input = state["user_input"]
    resume_text = state.get("resume_text", "")
    description = ""

    if input_type == "job_url":
        job_data = scrape_job_posting(user_input)
        description = job_data.get("job_description", "")
        state["scraped_job_title"] = job_data.get("job_title", "")

    elif input_type == "company_website":
        job_data = scrape_job_posting(user_input)
        website_text = job_data.get("job_description", "")

        if website_text:
            prompt = f"""Based on this company website content and the applicant's background, write a realistic job description for a role they would likely apply for at this company.
            
Candidate Background:
{resume_text[:800]}

Website Content:
{website_text[:2000]}
"""
            description = llm.invoke(prompt).content
        state["scraped_job_title"] = job_data.get("job_title", "")

    elif input_type == "company_name":
        prompt = f"""Write a realistic job description for a professional role at {user_input} that matches this candidate's background. 
If the candidate's background is in a specific field (e.g. Biomedical), ensure the role is relevant to that field.

Candidate Background:
{resume_text[:1000]}
"""
        description = llm.invoke(prompt).content

    elif input_type == "job_description":
        description = user_input

    if not description or len(description.strip()) < 50:
        description = FALLBACK_DESCRIPTION

    state["job_description"] = description
    state["job_skills"] = _extract_skills_from_text(description)
    return state