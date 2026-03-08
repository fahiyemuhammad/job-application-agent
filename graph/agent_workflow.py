from langgraph.graph import StateGraph, END

from agents.input_router import input_router
from agents.resume_analyzer import resume_analyzer
from agents.job_researcher import job_researcher
from agents.application_generator import application_generator
from agents.critic_agent import critic_agent
from graph.state import AgentState


def build_graph():
    """
    Graph flow:
      input_router
          ↓
      resume_analyzer  ──┐
                         ├──→ application_generator → critic_agent → END
      job_researcher   ──┘

    resume_analyzer and job_researcher run in parallel via fan-out from input_router.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("input_router", input_router)
    workflow.add_node("resume_analyzer", resume_analyzer)
    workflow.add_node("job_researcher", job_researcher)
    workflow.add_node("application_generator", application_generator)
    workflow.add_node("critic_agent", critic_agent)

    # Fan-out: run resume analysis and job research in parallel
    workflow.set_entry_point("input_router")
    workflow.add_edge("input_router", "resume_analyzer")
    workflow.add_edge("input_router", "job_researcher")

    # Fan-in: both must complete before generating the cover letter
    workflow.add_edge("resume_analyzer", "application_generator")
    workflow.add_edge("job_researcher", "application_generator")

    workflow.add_edge("application_generator", "critic_agent")
    workflow.add_edge("critic_agent", END)

    return workflow.compile()