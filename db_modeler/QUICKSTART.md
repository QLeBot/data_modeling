# Quick Start Guide

## Setup

1. **Install Python dependencies:**
   ```bash
   cd db_modeler
   pip install -r requirements.txt
   ```

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Snowflake credentials and API keys
   ```

## Running the Application

### Option 1: Using Make (Recommended)
```bash
# Terminal 1 - Backend
make run-backend

# Terminal 2 - Frontend
make run-frontend
```

### Option 2: Manual
```bash
# Terminal 1 - Backend
python run.py

# Terminal 2 - Frontend
cd frontend
npm start
```

## Usage

1. **Open browser:** http://localhost:3000

2. **Connect to Snowflake:**
   - Go to "Connection" tab
   - Enter your Snowflake credentials
   - Click "Connect to Snowflake"

3. **Reverse Engineer Schema:**
   - Go to "Reverse Engineer" tab
   - Enter database and schema name (e.g., `DB_PROD`, `BRONZE`)
   - Click "Reverse Engineer"

4. **Generate with AI:**
   - Go to "AI Design" tab
   - Describe your schema needs
   - Select schema type (Star/Snowflake)
   - Click "Generate Schema with AI"

5. **View Diagrams:**
   - Go to "Diagrams" tab
   - View ER diagram (Mermaid format)

6. **Generate dbt Models:**
   - Go to "dbt Models" tab
   - Click "Generate dbt Models"
   - Export models to files

## Using with Cursor AI

The tool is designed to work with Cursor's AI capabilities:

1. **AI Schema Generation:** Uses OpenAI/Anthropic APIs (configured in `.env`)
2. **Natural Language:** Describe schemas in plain English
3. **Context Aware:** AI understands your existing schemas

## Integration with Snowflake MCP Server

If you have Snowflake MCP server running:

1. Set `MCP_SERVER_ENABLED=true` in `.env`
2. Set `MCP_SERVER_URL` to your MCP server endpoint
3. The connector will automatically use MCP server when available

## Troubleshooting

- **Connection issues:** Check Snowflake credentials in `.env`
- **AI not working:** Verify `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in `.env`
- **Frontend not loading:** Ensure backend is running on port 8000
- **Import errors:** Make sure you're in the `db_modeler` directory when running
