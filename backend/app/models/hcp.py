from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    specialty = Column(String(200))        # e.g., "Cardiology", "Oncology"
    affiliation = Column(String(300))      # Hospital/Clinic name
    email = Column(String(200))
    phone = Column(String(50))

    # Relationship
    interactions = relationship("Interaction", back_populates="hcp")
