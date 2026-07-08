from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.graph import run_agent

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint. Receives user message + current form state,
    runs LangGraph agent, returns AI reply + form updates.
    """
    result = run_agent(
        user_message=request.message,
        current_form_data=request.current_form_data or {},
        interaction_id=request.interaction_id,
        db=db,
    )

    return ChatResponse(
        reply=result["reply"],
        form_updates=result.get("form_updates"),
        tool_used=result.get("tool_used"),
        interaction_id=result.get("interaction_id"),
    )
