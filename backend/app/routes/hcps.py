from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPResponse

router = APIRouter(tags=["HCPs"])

@router.get("/hcps", response_model=List[HCPResponse])
def list_hcps(
    search: Optional[str] = Query(None, description="Search HCPs by name"),
    db: Session = Depends(get_db)
):
    query = db.query(HCP)
    if search:
        query = query.filter(HCP.name.ilike(f"%{search}%"))
    return query.all()

@router.get("/hcps/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp
