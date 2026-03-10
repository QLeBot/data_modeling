# Installation Guide

## Quick Install (Recommended)

The basic installation works without optional dependencies:

```bash
cd db_modeler
pip install -r requirements.txt
cd frontend
npm install
```

## Optional Dependencies

### PostgreSQL Support (Optional)

If you want to use PostgreSQL for metadata storage instead of in-memory storage:

**Windows:**
1. Install PostgreSQL from https://www.postgresql.org/download/windows/
2. Add PostgreSQL `bin` directory to your PATH
3. Install: `pip install psycopg2-binary`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install libpq-dev
pip install psycopg2-binary

# macOS
brew install postgresql
pip install psycopg2-binary
```

### Graphviz Support (Optional)

For Graphviz diagram generation (Mermaid is used by default, no extra install needed):

**Windows:**
1. Download from https://graphviz.org/download/
2. Install and add to PATH
3. Install: `pip install graphviz pygraphviz`

**Linux:**
```bash
sudo apt-get install graphviz libgraphviz-dev
pip install graphviz pygraphviz
```

**macOS:**
```bash
brew install graphviz
pip install graphviz pygraphviz
```

## Troubleshooting

### psycopg2-binary Installation Issues

If you get errors installing `psycopg2-binary`:
- **Solution 1:** Skip it - the app works fine without it (uses in-memory storage)
- **Solution 2:** Install PostgreSQL first, then retry
- **Solution 3:** Use pre-built wheel: `pip install psycopg2-binary --only-binary :all:`

### Graphviz Issues

If you get Graphviz errors:
- **Solution:** Skip it - Mermaid diagrams work without Graphviz
- The frontend renders Mermaid diagrams directly in the browser

## Minimal Installation

For the absolute minimum to get started:

```bash
# Backend (core dependencies only)
pip install fastapi uvicorn pydantic pydantic-settings snowflake-connector-python openai python-dotenv jinja2

# Frontend
cd frontend
npm install
```

This will work for:
- ✅ Snowflake connections
- ✅ AI schema generation
- ✅ Mermaid diagrams
- ✅ dbt model generation
- ✅ In-memory model storage
