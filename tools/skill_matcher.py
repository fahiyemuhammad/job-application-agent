from difflib import SequenceMatcher


def _normalize(skill: str) -> str:
    return skill.lower().strip()


def _fuzzy_match(a: str, b: str, threshold: float = 0.82) -> bool:
    """Returns True if two skill strings are similar enough."""
    a, b = _normalize(a), _normalize(b)
    if a == b:
        return True
    if a in b or b in a:
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