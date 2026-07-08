from app.database import SessionLocal, engine, Base
from app.models import HCP, Material

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if already seeded
    if db.query(HCP).first():
        print("Database already seeded.")
        db.close()
        return

    # Seed HCPs
    hcps = [
        HCP(name="Dr. Sarah Smith", specialty="Cardiology", affiliation="City Heart Hospital"),
        HCP(name="Dr. John Chen", specialty="Oncology", affiliation="National Cancer Institute"),
        HCP(name="Dr. Emily Davis", specialty="Neurology", affiliation="Brain Health Clinic"),
        HCP(name="Dr. Michael Brown", specialty="Endocrinology", affiliation="Metro General Hospital"),
        HCP(name="Dr. Priya Patel", specialty="Pulmonology", affiliation="Lung Care Center"),
        HCP(name="Dr. Robert Wilson", specialty="Rheumatology", affiliation="Joint & Spine Clinic"),
        HCP(name="Dr. Lisa Anderson", specialty="Dermatology", affiliation="SkinFirst Medical"),
        HCP(name="Dr. James Taylor", specialty="Pediatrics", affiliation="Children's Medical Center"),
    ]
    db.add_all(hcps)

    # Seed Materials
    materials = [
        Material(name="Product X Efficacy Brochure", type="Brochure", description="Clinical data on Product X"),
        Material(name="Product Y Safety Profile", type="Clinical Study", description="Phase III safety data"),
        Material(name="Disease Awareness Pamphlet", type="Brochure", description="Patient education material"),
        Material(name="Dosing Guide Card", type="Reference Card", description="Quick dosing reference"),
        Material(name="Product X Samples (10mg)", type="Sample", description="Starter pack samples"),
        Material(name="Product Y Samples (25mg)", type="Sample", description="Trial samples"),
        Material(name="Clinical Trial Results Poster", type="Poster", description="Key results from Phase III"),
        Material(name="Comparison Chart vs Competitor", type="Brochure", description="Head-to-head comparison data"),
    ]
    db.add_all(materials)

    db.commit()
    db.close()
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    seed()
