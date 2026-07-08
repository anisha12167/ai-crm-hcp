import json
import logging
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.tools import ALL_TOOLS, search_hcp
from app.agent.prompts import SYSTEM_PROMPT
from app.config import settings
from app.models.hcp import HCP

logger = logging.getLogger(__name__)


def create_llm():
    """Initialize the Groq LLM with tool-calling capability."""
    return ChatGroq(
        model=settings.LLM_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.1,  # Low temp for reliable extraction
        max_tokens=1024,
    )


def create_graph(db=None):
    """Build the LangGraph StateGraph with all tools."""

    llm = create_llm()

    # Bind tools to the LLM — this tells the model what tools are available
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # ---- NODE: Agent (LLM decides what to do) ----
    def agent_node(state: AgentState) -> dict:
        """The LLM reads messages and decides whether to call a tool or respond."""
        # Build system message with current form context
        system_msg = SystemMessage(
            content=SYSTEM_PROMPT.format(
                current_form_data=json.dumps(state.get("form_data", {}), indent=2, default=str)
            )
        )
        messages = [system_msg] + state["messages"]

        try:
            response = llm_with_tools.invoke(messages)
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}. Falling back to {settings.LLM_FALLBACK_MODEL}")
            # Fallback to llama-3.3 if gemma2 fails
            fallback_llm = ChatGroq(
                model=settings.LLM_FALLBACK_MODEL,
                api_key=settings.GROQ_API_KEY,
                temperature=0.1,
                max_tokens=1024,
            ).bind_tools(ALL_TOOLS)
            response = fallback_llm.invoke(messages)

        return {"messages": [response]}

    # ---- NODE: Tool Execution ----
    def tool_node(state: AgentState) -> dict:
        """Execute the tool that the LLM decided to call."""
        last_message = state["messages"][-1]
        tool_calls = last_message.tool_calls

        results = []
        form_updates = {}
        tool_used = None

        for tc in tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            tool_used = tool_name

            logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

            # Special handling for search_hcp — needs DB access
            if tool_name == "search_hcp" and db:
                query = tool_args.get("query", "")
                hcps = db.query(HCP).filter(
                    HCP.name.ilike(f"%{query}%") |
                    HCP.specialty.ilike(f"%{query}%")
                ).limit(5).all()

                hcp_results = [
                    {"id": h.id, "name": h.name, "specialty": h.specialty, "affiliation": h.affiliation}
                    for h in hcps
                ]
                result_str = json.dumps({
                    "status": "success",
                    "action": "search_hcp",
                    "results": hcp_results,
                    "message": f"Found {len(hcp_results)} HCPs matching '{query}'"
                })
            else:
                # Find and execute the tool
                tool_fn = next((t for t in ALL_TOOLS if t.name == tool_name), None)
                if tool_fn:
                    result_str = tool_fn.invoke(tool_args)
                else:
                    result_str = json.dumps({"status": "error", "message": f"Unknown tool: {tool_name}"})

            # Parse the result to extract form_updates
            try:
                result_data = json.loads(result_str)
                if "form_data" in result_data:
                    form_updates.update(result_data["form_data"])
            except json.JSONDecodeError:
                pass

            results.append(
                ToolMessage(content=result_str, tool_call_id=tc["id"])
            )

        return {
            "messages": results,
            "form_updates": form_updates if form_updates else None,
            "tool_used": tool_used,
        }

    # ---- CONDITIONAL EDGE: Should we call a tool or end? ----
    def should_continue(state: AgentState) -> str:
        """Check if the LLM wants to call a tool."""
        last_message = state["messages"][-1]
        # If the LLM returned tool_calls, route to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        # Otherwise, end the graph
        return END

    # ---- BUILD THE GRAPH ----
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # Set entry point
    graph.set_entry_point("agent")

    # Add conditional edges from agent
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        }
    )

    # After tools execute, go back to agent (so it can read the result and respond)
    graph.add_edge("tools", "agent")

    # Compile the graph
    return graph.compile()


def run_agent(user_message: str, current_form_data: dict, interaction_id: int = None, db=None) -> dict:
    """
    Main entry point: run the LangGraph agent with a user message.

    Returns dict with: reply, form_updates, tool_used, interaction_id
    """
    graph = create_graph(db=db)

    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=user_message)],
        "form_data": current_form_data,
        "form_updates": None,
        "tool_used": None,
        "interaction_id": interaction_id,
    }

    # Run the graph
    result = graph.invoke(initial_state)

    # Extract the final AI message
    ai_messages = [
        m for m in result["messages"]
        if isinstance(m, AIMessage) and m.content and not m.tool_calls
    ]

    reply = ai_messages[-1].content if ai_messages else "I've processed your request."

    return {
        "reply": reply,
        "form_updates": result.get("form_updates"),
        "tool_used": result.get("tool_used"),
        "interaction_id": result.get("interaction_id"),
    }
