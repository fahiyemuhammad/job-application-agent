import os
import json
from langchain_groq import ChatGroq
from tools.job_scraper import scrape_job_posting
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=key , model="llama-3.1-8b-instant", temperature=0)

FALLBACK_DESCRIPTION = (
    "Software engineer role requiring Python, REST APIs, cloud platforms, "
    "and collaborative problem solving in an Agile environment."
)


def _extract_skills_from_text(description: str) -> list:
    """Ask LLM to extract & normalize job skills from a description."""
    prompt = f"""You are a job requirements parser. Extract ALL required and preferred technical skills from the job description below.

Normalize skill names to their full, common form (e.g. "AWS" → "Amazon Web Services (AWS)", "K8s" → "Kubernetes").

Return ONLY a valid JSON array of strings. No explanation, no markdown, no extra text.

Example output: ["Python", "Microsoft Azure", "Kubernetes", "Agile", "REST APIs"]

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
    Handles: job_url, company_website, company_name, job_description.
    """
    input_type = state["input_type"]
    user_input = state["user_input"]
    description = ""

    if input_type == "job_url":
        job_data = scrape_job_posting(user_input)
        description = job_data.get("job_description", "")
        state["scraped_job_title"] = job_data.get("job_title", "")

    elif input_type == "company_website":
        job_data = scrape_job_posting(user_input)
        website_text = job_data.get("job_description", "")

        if website_text:
            prompt = f"""Based on this company website content, write a realistic job description for a typical technical role at this company.
Include: role responsibilities, required skills, and company context.

Website Content:
{website_text}
"""
            description = llm.invoke(prompt).content
        state["scraped_job_title"] = job_data.get("job_title", "")

    elif input_type == "company_name":
        prompt = f"""Write a realistic and detailed job description for a typical mid-level technical role at {user_input}.
Include: company background, role overview, responsibilities, required skills, and nice-to-haves.
Make it sound like a real job posting.
"""
        description = llm.invoke(prompt).content

    elif input_type == "job_description":
        description = user_input

    if not description or len(description.strip()) < 50:
        description = FALLBACK_DESCRIPTION

    state["job_description"] = description
    state["job_skills"] = _extract_skills_from_text(description)
    return state