"""
Setup script for DB Modeler
"""
from setuptools import setup, find_packages

setup(
    name="db-modeler",
    version="0.1.0",
    description="Database modeling tool for Snowflake with AI assistance",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "snowflake-connector-python>=3.7.0",
        "openai>=1.3.5",
        "anthropic>=0.7.8",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.2",
    ],
    python_requires=">=3.10",
)
