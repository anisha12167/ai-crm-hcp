from pydantic import BaseModel
from typing import Optional

class MaterialResponse(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
