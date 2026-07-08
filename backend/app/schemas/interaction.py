from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class InteractionCreate(BaseModel):
    hcp_name: Optional[str] = None
    hcp_id: Optional[int] = None
    interaction_type: Optional[str] = "Meeting"
    date: Optional[date] = None
    time: Optional[time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None
    materials: Optional[List[str]] = []

class InteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None
    materials: Optional[List[str]] = None

class InteractionResponse(BaseModel):
    id: int
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None
    materials: List[str] = []

    class Config:
        from_attributes = True
