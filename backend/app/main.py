from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, inventory, training, content, integration, dashboard

import logging

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Tables (Simplistic migration)
try:
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

app = FastAPI(title="Project SAMARTH API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow Vercel Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas, models

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        user = crud.get_user_by_username(db, "admin")
        if not user:
            print("Creating Initial Super Admin...")
            admin_data = schemas.UserCreate(
                username="admin",
                password="admin123",
                full_name="Administrator",
                role=models.Role.SUPER_ADMIN
            )
            crud.create_user(db, admin_data)
            print("Super Admin Created: admin / admin123")
    finally:
        db.close()

# Include Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(integration.router, prefix="/api/v1/integration", tags=["integration"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Project SAMARTH API is running"}
