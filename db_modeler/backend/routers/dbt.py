"""
dbt model generation router
Generates dbt models from database schemas
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from dbt.generator import DBTModelGenerator

router = APIRouter()


class DBTModelRequest(BaseModel):
    """dbt model generation request"""
    database: str
    schema: str
    tables: Optional[List[str]] = None  # If None, generate all tables
    output_path: Optional[str] = None
    model_type: str = "view"  # view, table, incremental
    materialization: Optional[str] = None


class DBTModelConfig(BaseModel):
    """dbt model configuration"""
    name: str
    description: Optional[str] = None
    columns: List[Dict[str, any]]
    tests: Optional[List[Dict[str, str]]] = None
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, any]] = None


@router.post("/generate-models")
async def generate_dbt_models(request: DBTModelRequest):
    """Generate dbt models from Snowflake schema"""
    try:
        generator = DBTModelGenerator()
        models = generator.generate_from_schema(
            database=request.database,
            schema=request.schema,
            tables=request.tables,
            model_type=request.model_type,
            materialization=request.materialization
        )
        
        return {
            "models": models,
            "count": len(models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-model")
async def generate_single_dbt_model(model: DBTModelConfig):
    """Generate a single dbt model from configuration"""
    try:
        generator = DBTModelGenerator()
        model_code = generator.generate_model(
            name=model.name,
            description=model.description,
            columns=model.columns,
            tests=model.tests,
            tags=model.tags,
            meta=model.meta
        )
        
        return {
            "model": model_code,
            "name": model.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_dbt_models(
    models: List[Dict[str, any]],
    output_path: str
):
    """Export dbt models to files"""
    try:
        generator = DBTModelGenerator()
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        exported = []
        for model in models:
            file_path = output_dir / f"{model['name']}.sql"
            file_path.write_text(model['code'])
            exported.append(str(file_path))
        
        return {
            "exported": exported,
            "count": len(exported)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_dbt_templates():
    """Get available dbt model templates"""
    return {
        "templates": [
            {
                "name": "base",
                "description": "Basic dbt model",
                "type": "view"
            },
            {
                "name": "incremental",
                "description": "Incremental model",
                "type": "incremental"
            },
            {
                "name": "table",
                "description": "Materialized table",
                "type": "table"
            },
            {
                "name": "ephemeral",
                "description": "Ephemeral model",
                "type": "ephemeral"
            }
        ]
    }
