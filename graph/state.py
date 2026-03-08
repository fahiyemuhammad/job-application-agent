from typing import TypedDict, List, Dict, Annotated


def _keep_last(a, b):
    """Last writer wins — used for strings and dicts written by only one node."""
    return b if b else a


def _merge_lists(a: list, b: list) -> list:
    """Keep whichever list is non-empty; used for skill lists."""
    return b if b else a


class AgentState(TypedDict):
    # Input — set once before graph starts
    resume_text: Annotated[str, _keep_last]
    user_input: Annotated[str, _keep_last]

    # Routing
    input_type: Annotated[str, _keep_last]

    # Research
    job_description: Annotated[str, _keep_last]
    scraped_job_title: Annotated[str, _keep_last]

    # Analysis — resume_analyzer and job_researcher run in parallel,
    # each writes different keys, but LangGraph requires ALL keys to
    # have reducers when any parallel fan-out exists.
    personal_info: Annotated[Dict, _keep_last]
    resume_skills: Annotated[List[str], _merge_lists]
    job_skills: Annotated[List[str], _merge_lists]
    match_results: Annotated[Dict, _keep_last]

    # Output
    cover_letter: Annotated[str, _keep_last]
    improved_cover_letter: Annotated[str, _keep_last]