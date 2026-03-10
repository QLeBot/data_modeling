"""
Model management router
Store and retrieve database models
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter()

# In-memory storage (replace with database in production)
# For production, you can use SQLite (no extra dependencies) or PostgreSQL
models_storage: Dict[str, Dict] = {}


class ModelDefinition(BaseModel):
    """Database model definition"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    database: str
    schema: str
    tables: List[Dict]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict] = None


@router.post("/create")
async def create_model(model: ModelDefinition):
    """Create a new model"""
    import uuid
    model.id = str(uuid.uuid4())
    model.created_at = datetime.now()
    model.updated_at = datetime.now()
    
    models_storage[model.id] = model.dict()
    return {"id": model.id, "model": model.dict()}


@router.get("/list")
async def list_models():
    """List all models"""
    return {"models": list(models_storage.values())}


@router.get("/{model_id}")
async def get_model(model_id: str):
    """Get a specific model"""
    if model_id not in models_storage:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"model": models_storage[model_id]}


@router.put("/{model_id}")
async def update_model(model_id: str, model: ModelDefinition):
    """Update a model"""
    if model_id not in models_storage:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model.updated_at = datetime.now()
    models_storage[model_id] = model.dict()
    return {"model": models_storage[model_id]}


@router.delete("/{model_id}")
async def delete_model(model_id: str):
    """Delete a model"""
    if model_id not in models_storage:
        raise HTTPException(status_code=404, detail="Model not found")
    
    del models_storage[model_id]
    return {"status": "deleted"}
