from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

# Many-to-many junction table
interaction_materials = Table(
    "interaction_materials",
    Base.metadata,
    Column("interaction_id", Integer, ForeignKey("interactions.id"), primary_key=True),
    Column("material_id", Integer, ForeignKey("materials.id"), primary_key=True),
)

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=True)
    hcp_name = Column(String(200))  # Denormalized for quick access
    interaction_type = Column(String(50), default="Meeting")  # Meeting, Call, Email, Video Conference
    date = Column(Date, default=datetime.date.today)
    time = Column(Time, default=datetime.datetime.now().time)
    attendees = Column(Text)  # Comma-separated or JSON string
    topics_discussed = Column(Text)
    sentiment = Column(String(50))  # Positive, Negative, Neutral
    notes = Column(Text)
    follow_up = Column(Text)

    # Relationships
    hcp = relationship("HCP", back_populates="interactions")
    materials = relationship("Material", secondary=interaction_materials, back_populates="interactions")
