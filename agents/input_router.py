import re
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Patterns that strongly suggest a direct job posting URL
JOB_URL_PATTERNS = re.compile(
    r"(jobs|careers|job|career|position|vacancy|opening|posting|apply|recruitment|hire)",
    re.IGNORECASE,
)


def input_router(state: dict) -> dict:
    """
    Classifies user input as one of:
      - job_url        → direct link to a job posting
      - company_website → company homepage/about page
      - company_name   → plain company name text
      - job_description → pasted job description text
    """
    user_input = state["user_input"].strip()

    # --- URL detection ---
    if re.match(r"https?://", user_input):
        if JOB_URL_PATTERNS.search(user_input):
            state["input_type"] = "job_url"
        else:
            state["input_type"] = "company_website"
        return state

    # --- LLM classification for non-URL text ---
    prompt = f"""Classify the following user input into exactly one of these categories:
- company_name   (just a company name, e.g. "Google", "Anthropic")
- job_description (a pasted block of text describing a job role)

Reply with only the category label, nothing else.

Input:
\"\"\"{user_input}\"\"\"
"""
    response = llm.invoke(prompt)
    label = response.content.strip().lower()

    # Sanitize — only accept known labels
    if label not in ("company_name", "job_description"):
        # Heuristic fallback: if it's long it's probably a description
        label = "job_description" if len(user_input.split()) > 20 else "company_name"

    state["input_type"] = label
    return state