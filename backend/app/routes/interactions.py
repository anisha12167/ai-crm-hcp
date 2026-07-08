from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.interaction import Interaction
from app.models.material import Material
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionResponse
import datetime

router = APIRouter(tags=["Interactions"])

def _interaction_to_response(interaction: Interaction) -> dict:
    return {
        "id": interaction.id,
        "hcp_name": interaction.hcp_name,
        "interaction_type": interaction.interaction_type,
        "date": interaction.date,
        "time": interaction.time,
        "attendees": interaction.attendees,
        "topics_discussed": interaction.topics_discussed,
        "sentiment": interaction.sentiment,
        "notes": interaction.notes,
        "follow_up": interaction.follow_up,
        "materials": [m.name for m in interaction.materials] if interaction.materials else [],
    }

@router.get("/interactions", response_model=List[InteractionResponse])
def list_interactions(db: Session = Depends(get_db)):
    interactions = db.query(Interaction).order_by(Interaction.id.desc()).all()
    return [_interaction_to_response(i) for i in interactions]

@router.get("/interactions/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return _interaction_to_response(interaction)

@router.post("/interactions", response_model=InteractionResponse)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    interaction = Interaction(
        hcp_name=data.hcp_name,
        hcp_id=data.hcp_id,
        interaction_type=data.interaction_type or "Meeting",
        date=data.date or datetime.date.today(),
        time=data.time or datetime.datetime.now().time(),
        attendees=data.attendees,
        topics_discussed=data.topics_discussed,
        sentiment=data.sentiment,
        notes=data.notes,
        follow_up=data.follow_up,
    )

    # Handle materials
    if data.materials:
        for mat_name in data.materials:
            material = db.query(Material).filter(Material.name.ilike(f"%{mat_name}%")).first()
            if material:
                interaction.materials.append(material)

    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return _interaction_to_response(interaction)

@router.put("/interactions/{interaction_id}", response_model=InteractionResponse)
def update_interaction(interaction_id: int, data: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle materials separately
    materials_list = update_data.pop("materials", None)

    for field, value in update_data.items():
        if value is not None:
            setattr(interaction, field, value)

    if materials_list is not None:
        interaction.materials.clear()
        for mat_name in materials_list:
            material = db.query(Material).filter(Material.name.ilike(f"%{mat_name}%")).first()
            if material:
                interaction.materials.append(material)

    db.commit()
    db.refresh(interaction)
    return _interaction_to_response(interaction)

@router.delete("/interactions/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    db.delete(interaction)
    db.commit()
    return {"message": "Interaction deleted"}
