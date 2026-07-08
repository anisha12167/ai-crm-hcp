from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import hcps, interactions, chat, materials
from app.database import engine, Base

# Create tables (use Alembic in production, this is fine for demo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module", version="1.0.0")

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hcps.router, prefix="/api")
app.include_router(interactions.router, prefix="/api")
app.include_router(materials.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI-First CRM HCP Module API"}
