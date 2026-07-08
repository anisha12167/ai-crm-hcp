from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The state that flows through the LangGraph.

    - messages: Full conversation history (LangGraph manages appending via add_messages)
    - form_data: Current form state from the frontend (used by tools to know what's already filled)
    - form_updates: Dict of field changes to send back to frontend (tools write here)
    - tool_used: Name of the last tool invoked (for frontend to know what happened)
    - interaction_id: DB ID of the current interaction (for edit/delete operations)
    """
    messages: Annotated[list, add_messages]
    form_data: dict
    form_updates: Optional[dict]
    tool_used: Optional[str]
    interaction_id: Optional[int]
