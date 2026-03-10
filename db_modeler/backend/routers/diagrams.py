"""
Diagram generation router
Supports Mermaid and Graphviz formats
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from diagrams.generators import MermaidGenerator, GraphvizGenerator

router = APIRouter()


class TableSchema(BaseModel):
    """Table schema definition"""
    name: str
    columns: List[Dict[str, any]]
    primary_key: Optional[List[str]] = None
    foreign_keys: Optional[List[Dict[str, str]]] = None


class DiagramRequest(BaseModel):
    """Diagram generation request"""
    tables: List[TableSchema]
    format: str = "mermaid"  # mermaid or graphviz
    style: str = "er"  # er, star, snowflake


@router.post("/generate")
async def generate_diagram(request: DiagramRequest):
    """Generate ER diagram from schema"""
    try:
        if request.format == "mermaid":
            generator = MermaidGenerator()
            diagram = generator.generate_er_diagram(request.tables, request.style)
        elif request.format == "graphviz":
            generator = GraphvizGenerator()
            diagram = generator.generate_er_diagram(request.tables, request.style)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.format}")
        
        return {
            "diagram": diagram,
            "format": request.format,
            "style": request.style
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-schema")
async def generate_from_schema(
    database: str,
    schema: str,
    format: str = "mermaid",
    style: str = "er"
):
    """Generate diagram from reverse-engineered schema"""
    # This will call the snowflake router to get schema, then generate diagram
    # Implementation will be added
    pass


@router.get("/preview/{diagram_id}")
async def preview_diagram(diagram_id: str):
    """Get diagram preview URL"""
    # Generate preview image or return diagram code
    pass
