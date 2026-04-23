import re
from difflib import SequenceMatcher


def _normalize(skill: str) -> str:
    return skill.lower().strip()


def _fuzzy_match(a: str, b: str, threshold: float = 0.90) -> bool:
    """Returns True if two skill strings are similar enough, with precision for distinct languages."""
    a, b = _normalize(a), _normalize(b)
    if a == b:
        return True
    
    # Specific guards for common distinct languages/tools that are substrings
    distinct_pairs = [
        {"java", "javascript"},
        {"c", "c++"},
        {"c", "c#"},
        {"sql", "nosql"},
        {"python", "cython"},
    ]
    for pair in distinct_pairs:
        if a in pair and b in pair:
            return False

    # Check for inclusion with word boundaries or common extensions
    a_clean = a.replace(".js", "").replace(".py", "").strip()
    b_clean = b.replace(".js", "").replace(".py", "").strip()
    if a_clean == b_clean:
        return True

    # Check if one is a whole word in the other
    pattern = r"\b" + re.escape(a) + r"\b"
    if re.search(pattern, b) or re.search(r"\b" + re.escape(b) + r"\b", a):
        return True

    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio >= threshold


def match_skills(resume_skills: list, job_skills: list) -> dict:
    """
    Matches resume skills to job skills using fuzzy matching.
    Much more robust than exact set intersection.
    """
    matched = []
    missing = []

    for job_skill in job_skills:
        found = False
        for resume_skill in resume_skills:
            if _fuzzy_match(job_skill, resume_skill):
                matched.append(job_skill)
                found = True
                break
        if not found:
            missing.append(job_skill)

    score = 0.0
    if job_skills:
        score = round((len(matched) / len(job_skills)) * 100, 1)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score,
    }