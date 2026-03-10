"""
Snowflake integration router
Supports both MCP server and direct Python connector
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from snowflake.connector import connect
from snowflake.integrations.snowflake_connector import SnowflakeConnector

router = APIRouter()


class SnowflakeConnection(BaseModel):
    """Snowflake connection parameters"""
    account: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    warehouse: Optional[str] = None
    database: Optional[str] = None
    schema: Optional[str] = None
    role: Optional[str] = None


class QueryRequest(BaseModel):
    """SQL query request"""
    query: str
    connection: Optional[SnowflakeConnection] = None


def get_default_connection() -> SnowflakeConnection:
    """Get connection from environment variables"""
    return SnowflakeConnection(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def get_connection(conn_params: SnowflakeConnection) -> Any:
    """Create Snowflake connection"""
    params = conn_params.dict(exclude_none=True)
    if not params.get("account"):
        raise HTTPException(status_code=400, detail="Snowflake account is required")
    
    try:
        return connect(**params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")


@router.post("/connect")
async def connect_snowflake(connection: SnowflakeConnection):
    """Test Snowflake connection"""
    try:
        conn = get_connection(connection)
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"status": "connected", "snowflake_version": version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/databases")
async def list_databases(connection: Optional[SnowflakeConnection] = None):
    """List all databases"""
    conn_params = connection or get_default_connection()
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[1] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"databases": databases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schemas")
async def list_schemas(
    database: Optional[str] = None,
    connection: Optional[SnowflakeConnection] = None
):
    """List schemas in a database"""
    conn_params = connection or get_default_connection()
    if database:
        conn_params.database = database
    
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        if database:
            cursor.execute(f"SHOW SCHEMAS IN DATABASE {database}")
        else:
            cursor.execute("SHOW SCHEMAS")
        schemas = [row[1] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"schemas": schemas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables")
async def list_tables(
    database: Optional[str] = None,
    schema: Optional[str] = None,
    connection: Optional[SnowflakeConnection] = None
):
    """List tables in a schema"""
    conn_params = connection or get_default_connection()
    if database:
        conn_params.database = database
    if schema:
        conn_params.schema = schema
    
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        query = "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES"
        conditions = []
        if database:
            conditions.append(f"TABLE_CATALOG = '{database}'")
        if schema:
            conditions.append(f"TABLE_SCHEMA = '{schema}'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY TABLE_SCHEMA, TABLE_NAME"
        
        cursor.execute(query)
        tables = [
            {"schema": row[0], "name": row[1], "type": row[2]}
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/columns")
async def get_table_columns(
    database: str,
    schema: str,
    table: str,
    connection: Optional[SnowflakeConnection] = None
):
    """Get columns for a specific table"""
    conn_params = connection or get_default_connection()
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_CATALOG = %s
              AND TABLE_SCHEMA = %s
              AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (database, schema, table))
        
        columns = [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "default": row[3],
                "comment": row[4]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reverse-engineer")
async def reverse_engineer_schema(
    database: str,
    schema: str,
    connection: Optional[SnowflakeConnection] = None
):
    """Reverse engineer a complete schema"""
    conn_params = connection or get_default_connection()
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute(f"""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_CATALOG = '{database}'
              AND TABLE_SCHEMA = '{schema}'
              AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        schema_data = {
            "database": database,
            "schema": schema,
            "tables": []
        }
        
        # Get columns for each table
        for table in tables:
            cursor.execute(f"""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_CATALOG = '{database}'
                  AND TABLE_SCHEMA = '{schema}'
                  AND TABLE_NAME = '{table}'
                ORDER BY ORDINAL_POSITION
            """)
            
            columns = [
                {
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2] == "YES",
                    "default": row[3],
                    "comment": row[4]
                }
                for row in cursor.fetchall()
            ]
            
            schema_data["tables"].append({
                "name": table,
                "columns": columns
            })
        
        # Get foreign keys (if any)
        cursor.execute(f"""
            SELECT 
                FK_TABLE_NAME,
                FK_COLUMN_NAME,
                PK_TABLE_NAME,
                PK_COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
            WHERE tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
              AND tc.TABLE_CATALOG = '{database}'
              AND tc.TABLE_SCHEMA = '{schema}'
        """)
        
        # TODO: Parse foreign key relationships
        
        cursor.close()
        conn.close()
        return schema_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def execute_query(request: QueryRequest):
    """Execute a SQL query"""
    conn_params = request.connection or get_default_connection()
    conn = get_connection(conn_params)
    
    try:
        cursor = conn.cursor()
        cursor.execute(request.query)
        
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
        else:
            result = {"rows_affected": cursor.rowcount}
        
        cursor.close()
        conn.close()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
