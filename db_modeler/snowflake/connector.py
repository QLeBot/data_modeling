"""
Snowflake connector wrapper
Supports both direct connection and MCP server
"""
import os
from typing import Optional, Dict, Any, List
from snowflake.connector import connect, DictCursor


class SnowflakeConnector:
    """Unified Snowflake connector"""
    
    def __init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
        use_mcp: bool = False,
        mcp_url: Optional[str] = None
    ):
        self.account = account or os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = user or os.getenv("SNOWFLAKE_USER")
        self.password = password or os.getenv("SNOWFLAKE_PASSWORD")
        self.warehouse = warehouse or os.getenv("SNOWFLAKE_WAREHOUSE")
        self.database = database or os.getenv("SNOWFLAKE_DATABASE")
        self.schema = schema or os.getenv("SNOWFLAKE_SCHEMA")
        self.role = role
        self.use_mcp = use_mcp or os.getenv("MCP_SERVER_ENABLED", "false").lower() == "true"
        self.mcp_url = mcp_url or os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self._connection = None
    
    def connect(self):
        """Establish connection"""
        if self.use_mcp:
            return self._connect_via_mcp()
        else:
            return self._connect_direct()
    
    def _connect_direct(self):
        """Direct Snowflake connection"""
        params = {
            "account": self.account,
            "user": self.user,
            "password": self.password,
        }
        if self.warehouse:
            params["warehouse"] = self.warehouse
        if self.database:
            params["database"] = self.database
        if self.schema:
            params["schema"] = self.schema
        if self.role:
            params["role"] = self.role
        
        self._connection = connect(**params)
        return self._connection
    
    def _connect_via_mcp(self):
        """Connect via MCP server"""
        # MCP server connection will be implemented
        # For now, fallback to direct connection
        return self._connect_direct()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Execute a query and return results"""
        if not self._connection:
            self.connect()
        
        cursor = self._connection.cursor(DictCursor)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_schema_metadata(self, database: str, schema: str) -> Dict[str, Any]:
        """Get complete schema metadata"""
        tables_query = f"""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_CATALOG = '{database}'
              AND TABLE_SCHEMA = '{schema}'
              AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """
        
        tables = self.execute_query(tables_query)
        schema_data = {
            "database": database,
            "schema": schema,
            "tables": []
        }
        
        for table_row in tables:
            table_name = table_row["TABLE_NAME"]
            columns_query = f"""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_CATALOG = '{database}'
                  AND TABLE_SCHEMA = '{schema}'
                  AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """
            
            columns = self.execute_query(columns_query)
            schema_data["tables"].append({
                "name": table_name,
                "columns": columns
            })
        
        return schema_data
    
    def close(self):
        """Close connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
