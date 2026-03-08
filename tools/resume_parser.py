import pdfplumber
import re


def parse_resume(file_path: str) -> str:
    """
    Extracts text from a PDF resume.
    Returns the full text for LLM processing.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise Exception(f"Error parsing resume: {e}")
    return text


def extract_personal_info(resume_text: str) -> dict:
    """
    Extracts name, email, phone from resume text using regex heuristics.
    Used to fill cover letter placeholders.
    """
    info = {"name": "", "email": "", "phone": ""}

    # Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text)
    if email_match:
        info["email"] = email_match.group()

    # Phone (handles various formats)
    phone_match = re.search(
        r"(\+?\d[\d\s\-().]{7,}\d)", resume_text
    )
    if phone_match:
        info["phone"] = phone_match.group().strip()

    # Name: assume it's the first non-empty line of the resume
    lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
    if lines:
        first_line = lines[0]
        # Likely a name if it's short and has no digits
        if len(first_line.split()) <= 5 and not re.search(r"\d", first_line):
            info["name"] = first_line

    return info