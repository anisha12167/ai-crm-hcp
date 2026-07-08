from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.material import Material
import datetime


def create_interaction(db: Session, data: dict) -> Interaction:
    """Create a new interaction record in the database."""
    interaction = Interaction(
        hcp_name=data.get("hcp_name"),
        hcp_id=data.get("hcp_id"),
        interaction_type=data.get("interaction_type", "Meeting"),
        date=data.get("date", datetime.date.today()),
        time=data.get("time", datetime.datetime.now().time()),
        attendees=data.get("attendees"),
        topics_discussed=data.get("topics_discussed"),
        sentiment=data.get("sentiment"),
        notes=data.get("notes"),
        follow_up=data.get("follow_up"),
    )

    # Handle materials
    materials = data.get("materials", [])
    if materials:
        for mat_name in materials:
            material = db.query(Material).filter(Material.name.ilike(f"%{mat_name}%")).first()
            if material:
                interaction.materials.append(material)

    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def get_interaction_by_id(db: Session, interaction_id: int) -> Interaction:
    """Get a single interaction by ID."""
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def update_interaction(db: Session, interaction_id: int, data: dict) -> Interaction:
    """Update an existing interaction."""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return None

    for field, value in data.items():
        if field == "materials":
            interaction.materials.clear()
            for mat_name in value:
                material = db.query(Material).filter(Material.name.ilike(f"%{mat_name}%")).first()
                if material:
                    interaction.materials.append(material)
        elif value is not None and hasattr(interaction, field):
            setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)
    return interaction
