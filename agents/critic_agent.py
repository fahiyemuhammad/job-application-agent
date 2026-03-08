from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


def critic_agent(state: dict) -> dict:
    """
    Reviews and polishes the cover letter.
    Returns ONLY the improved letter — no meta-commentary or improvement lists.
    Uses a stronger model for final polish.
    """
    cover_letter = state["cover_letter"]
    job_description = state.get("job_description", "")
    match_score = state.get("match_results", {}).get("match_score", 0)

    prompt = f"""You are an expert career coach and editor. Your task is to polish the cover letter below.

JOB DESCRIPTION CONTEXT:
{job_description[:1500]}

MATCH SCORE: {match_score}% skill alignment

EDITING GUIDELINES:
- Strengthen the opening hook — make it immediately compelling
- Ensure specific, concrete examples are used (not vague claims)
- Remove any filler phrases ("I am writing to...", "I believe I would be...")  
- Tighten sentences — aim for impact over length
- Make sure NO placeholder text like [Your Name] or [Company] remains
- Verify the closing paragraph has a confident, specific call to action
- Keep the professional tone consistent throughout
- Do NOT add bullet points, headers, or sections — it must read as flowing prose
- Do NOT add any commentary, notes, or explanation after the letter
- Output ONLY the final polished cover letter, nothing else

COVER LETTER TO IMPROVE:
{cover_letter}
"""

    improved = llm.invoke(prompt)

    # Strip any trailing commentary the LLM might add despite instructions
    letter_text = improved.content.strip()

    # Heuristic: cut off anything after common commentary starters
    cutoff_phrases = [
        "improvements made",
        "changes made",
        "notes:",
        "here's what i changed",
        "explanation:",
        "i made the following",
    ]
    lower = letter_text.lower()
    for phrase in cutoff_phrases:
        idx = lower.find(phrase)
        if idx != -1:
            letter_text = letter_text[:idx].strip()

    state["improved_cover_letter"] = letter_text
    return state