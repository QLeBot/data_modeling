# DB Modeler - Snowflake Database Modeling Tool

A database modeling tool designed to work within Cursor IDE, with Snowflake integration and AI-powered schema generation.

## Features

- 🎨 Visual ER diagram generation
- ❄️ Native Snowflake integration (MCP server + Python connector)
- 🤖 AI-powered schema design (via Cursor AI)
- 📊 Star/Snowflake schema support
- 🔄 Reverse engineering from existing databases
- 📝 dbt model generation
- 🌐 Web-based frontend (runs in browser)

## Architecture

```
db_modeler/
├── backend/          # FastAPI backend
├── frontend/         # React web interface
├── snowflake/        # Snowflake integration
├── ai/              # AI schema generation
├── diagrams/        # Diagram generation (Mermaid/Graphviz)
├── dbt/             # dbt model generator
└── config/          # Configuration files
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- Snowflake account with credentials
- Cursor IDE

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your Snowflake credentials
```

### Running

```bash
# Start backend
python -m backend.main

# Start frontend (in another terminal)
cd frontend
npm start
```

Access the tool at: http://localhost:3000

## Usage

1. Connect to Snowflake via MCP server or Python connector
2. Reverse engineer existing schemas
3. Use AI to generate new schemas (via Cursor AI)
4. Visualize with ER diagrams
5. Export to dbt models

## Development

This tool is designed to work seamlessly with Cursor IDE's AI capabilities for schema design assistance.
