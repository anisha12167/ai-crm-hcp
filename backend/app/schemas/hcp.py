from pydantic import BaseModel
from typing import Optional

class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    affiliation: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class HCPResponse(HCPBase):
    id: int

    class Config:
        from_attributes = True
