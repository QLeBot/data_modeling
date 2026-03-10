"""
dbt model generator
Generates dbt models from database schemas
"""
from typing import List, Dict, Any, Optional
from jinja2 import Template
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from snowflake.connector import SnowflakeConnector


class DBTModelGenerator:
    """Generate dbt models"""
    
    MODEL_TEMPLATE = """-- dbt model: {{ model_name }}
-- Generated from {{ database }}.{{ schema }}.{{ table_name }}

{{ config(
    materialized='{{ materialization }}',
    {% if tags %}tags={{ tags }},{% endif %}
    {% if meta %}meta={{ meta }}{% endif %}
) }}

/*
{{ description }}
*/

select
{%- for column in columns %}
    {{ column.name }}{% if column.alias %} as {{ column.alias }}{% endif %}{% if not loop.last %},{% endif %}
{%- endfor %}
from {{ source('{{ source_name }}', '{{ table_name }}') }}
{% if where_clause %}
where {{ where_clause }}
{% endif %}
"""
    
    MODEL_WITH_TESTS_TEMPLATE = """-- dbt model: {{ model_name }}
-- Generated from {{ database }}.{{ schema }}.{{ table_name }}

{{ config(
    materialized='{{ materialization }}',
    {% if tags %}tags={{ tags }},{% endif %}
) }}

select
{%- for column in columns %}
    {{ column.name }}{% if column.alias %} as {{ column.alias }}{% endif %}{% if not loop.last %},{% endif %}
{%- endfor %}
from {{ source('{{ source_name }}', '{{ table_name }}') }}

{% if tests %}
{% for test in tests %}
-- Test: {{ test.name }}
-- {{ test.description }}
{% endfor %}
{% endif %}
"""
    
    def __init__(self):
        self.template = Template(self.MODEL_TEMPLATE)
    
    def generate_from_schema(
        self,
        database: str,
        schema: str,
        tables: Optional[List[str]] = None,
        model_type: str = "view",
        materialization: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Generate dbt models from Snowflake schema"""
        connector = SnowflakeConnector()
        schema_data = connector.get_schema_metadata(database, schema)
        
        models = []
        materialization = materialization or model_type
        
        for table in schema_data["tables"]:
            if tables and table["name"] not in tables:
                continue
            
            model_code = self.generate_model(
                name=table["name"],
                description=f"Model for {table['name']}",
                columns=[
                    {
                        "name": col["COLUMN_NAME"],
                        "type": col["DATA_TYPE"],
                        "nullable": col["IS_NULLABLE"] == "YES"
                    }
                    for col in table["columns"]
                ],
                materialization=materialization,
                source_name=schema,
                table_name=table["name"],
                database=database,
                schema=schema
            )
            
            models.append({
                "name": table["name"],
                "code": model_code,
                "database": database,
                "schema": schema
            })
        
        return models
    
    def generate_model(
        self,
        name: str,
        description: str,
        columns: List[Dict[str, Any]],
        materialization: str = "view",
        source_name: Optional[str] = None,
        table_name: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tests: Optional[List[Dict[str, str]]] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a single dbt model"""
        return self.template.render(
            model_name=name,
            description=description,
            columns=columns,
            materialization=materialization,
            source_name=source_name or name,
            table_name=table_name or name,
            database=database or "",
            schema=schema or "",
            tags=tags,
            tests=tests,
            meta=meta,
            where_clause=None
        )
    
    def generate_star_schema_models(
        self,
        fact_table: Dict,
        dim_tables: List[Dict],
        database: str,
        schema: str
    ) -> Dict[str, List[Dict[str, str]]]:
        """Generate dbt models for star schema"""
        models = {
            "fact": [],
            "dimensions": []
        }
        
        # Generate fact table model
        fact_model = self.generate_model(
            name=fact_table["name"],
            description=f"Fact table: {fact_table['name']}",
            columns=fact_table["columns"],
            materialization="table",
            tags=["fact"],
            database=database,
            schema=schema
        )
        models["fact"].append({
            "name": fact_table["name"],
            "code": fact_model
        })
        
        # Generate dimension models
        for dim in dim_tables:
            dim_model = self.generate_model(
                name=dim["name"],
                description=f"Dimension table: {dim['name']}",
                columns=dim["columns"],
                materialization="table",
                tags=["dimension"],
                database=database,
                schema=schema
            )
            models["dimensions"].append({
                "name": dim["name"],
                "code": dim_model
            })
        
        return models
