"""
main.py

Entry point for the Mafilika Business Automation Suite backend API.

Run locally with:
    uvicorn main:app --reload

This file:
1. Creates the FastAPI app
2. Configures CORS so the Netlify-hosted frontend can call this API
3. Creates database tables on startup (Phase 1 uses simple create_all;
   a migration tool like Alembic can be introduced in a later phase)
4. Registers all route modules (auth, profile)

Future modules (CRM, email automation, reports, files) will each get
their own file in app/routes/ and be included here with one extra line -
that's the whole point of this foundation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import Base, engine

# Import models so they are registered with SQLAlchemy's Base metadata
# before create_all() runs.
from app.models import user, company, activity  # noqa: F401

from app.routes import auth, profile

# --- Create database tables (Phase 1: simple approach) ---
Base.metadata.create_all(bind=engine)

# --- Create the FastAPI app ---
app = FastAPI(
    title=settings.APP_NAME,
    description="Foundation API for the Mafilika Business Automation Suite (Phase 1).",
    version="1.0.0",
)

# --- CORS configuration ---
# Allows the frontend (Netlify + local dev server) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register routes ---
app.include_router(auth.router)
app.include_router(profile.router)


@app.get("/", tags=["Health"])
def root():
    """Simple health check / welcome endpoint."""
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "message": "Mafilika Business Automation Suite API is running.",
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """Used by uptime monitors / deployment platforms to verify the API is alive."""
    return {"status": "healthy"}
