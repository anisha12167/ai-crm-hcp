from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.interaction import interaction_materials

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    type = Column(String(100))  # Brochure, Clinical Study, Sample, etc.
    description = Column(Text)

    interactions = relationship("Interaction", secondary=interaction_materials, back_populates="materials")
