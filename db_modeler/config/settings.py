"""
Configuration settings for DB Modeler
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Snowflake
    snowflake_account: str = ""
    snowflake_user: str = ""
    snowflake_password: str = ""
    snowflake_warehouse: str = ""
    snowflake_database: str = ""
    snowflake_schema: str = ""
    
    # MCP Server
    mcp_server_enabled: bool = False
    mcp_server_url: str = "http://localhost:8000"
    
    # AI
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Storage
    database_url: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
