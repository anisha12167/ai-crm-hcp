from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.material import Material
from app.schemas.material import MaterialResponse

router = APIRouter(tags=["Materials"])

@router.get("/materials", response_model=List[MaterialResponse])
def list_materials(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Material)
    if search:
        query = query.filter(Material.name.ilike(f"%{search}%"))
    return query.all()
