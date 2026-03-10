"""
AI-powered schema generation router
Uses OpenAI/Anthropic APIs for schema design
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from ai.schema_generator import AISchemaGenerator

router = APIRouter()


class AISchemaRequest(BaseModel):
    """AI schema generation request"""
    prompt: str
    existing_schema: Optional[Dict] = None
    schema_type: str = "star"  # star, snowflake, normalized
    provider: str = "openai"  # openai, anthropic


class AISchemaResponse(BaseModel):
    """AI-generated schema response"""
    schema: Dict
    explanation: str
    suggestions: Optional[List[str]] = None


@router.post("/generate-schema")
async def generate_schema(request: AISchemaRequest):
    """Generate database schema from natural language prompt"""
    try:
        generator = AISchemaGenerator(provider=request.provider)
        result = generator.generate_schema(
            prompt=request.prompt,
            existing_schema=request.existing_schema,
            schema_type=request.schema_type
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-improvements")
async def suggest_improvements(
    schema: Dict,
    provider: str = "openai"
):
    """Get AI suggestions for schema improvements"""
    try:
        generator = AISchemaGenerator(provider=provider)
        suggestions = generator.suggest_improvements(schema)
        
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-schema")
async def explain_schema(
    schema: Dict,
    provider: str = "openai"
):
    """Get AI explanation of a schema"""
    try:
        generator = AISchemaGenerator(provider=provider)
        explanation = generator.explain_schema(schema)
        
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate-schema")
async def validate_schema(
    schema: Dict,
    provider: str = "openai"
):
    """Validate schema design with AI"""
    try:
        generator = AISchemaGenerator(provider=provider)
        validation = generator.validate_schema(schema)
        
        return validation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
