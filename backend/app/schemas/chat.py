from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ChatRequest(BaseModel):
    message: str
    current_form_data: Optional[Dict[str, Any]] = None
    interaction_id: Optional[int] = None

class ChatResponse(BaseModel):
    reply: str
    form_updates: Optional[Dict[str, Any]] = None
    tool_used: Optional[str] = None
    interaction_id: Optional[int] = None
