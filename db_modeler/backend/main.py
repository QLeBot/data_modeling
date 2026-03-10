"""
Main FastAPI application for DB Modeler
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from backend.routers import snowflake, diagrams, dbt, ai, models

load_dotenv()

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 DB Modeler backend starting...")
    yield
    # Shutdown
    print("👋 DB Modeler backend shutting down...")


app = FastAPI(
    title="DB Modeler API",
    description="Database modeling tool for Snowflake with AI assistance",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(snowflake.router, prefix="/api/snowflake", tags=["snowflake"])
app.include_router(diagrams.router, prefix="/api/diagrams", tags=["diagrams"])
app.include_router(dbt.router, prefix="/api/dbt", tags=["dbt"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(models.router, prefix="/api/models", tags=["models"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "DB Modeler API",
        "version": "0.1.0"
    }


@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "snowflake_configured": bool(os.getenv("SNOWFLAKE_ACCOUNT")),
        "ai_configured": bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
