#!/usr/bin/env python3
"""
Main entry point for DB Modeler
Run this to start the backend server
"""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(
        "backend.main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=port,
        reload=True,
        log_level="info"
    )
