from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, inventory, training, content, integration, dashboard

# Create Tables (Simplistic migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project SAMARTH API", version="1.0.0")

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
