from sqlalchemy.orm import Session
from app.models.hcp import HCP
from typing import List


def search_hcps(db: Session, query: str, limit: int = 5) -> List[dict]:
    """Search HCPs by name or specialty."""
    hcps = db.query(HCP).filter(
        HCP.name.ilike(f"%{query}%") |
        HCP.specialty.ilike(f"%{query}%")
    ).limit(limit).all()

    return [
        {
            "id": h.id,
            "name": h.name,
            "specialty": h.specialty,
            "affiliation": h.affiliation,
        }
        for h in hcps
    ]


def get_hcp_by_name(db: Session, name: str) -> HCP:
    """Find an HCP by exact or partial name match."""
    return db.query(HCP).filter(HCP.name.ilike(f"%{name}%")).first()
