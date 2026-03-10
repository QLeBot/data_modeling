"""
Diagram generation for ER diagrams
Supports Mermaid and Graphviz formats
"""
from typing import List, Dict, Any


class MermaidGenerator:
    """Generate Mermaid ER diagrams"""
    
    def generate_er_diagram(self, tables: List[Dict], style: str = "er") -> str:
        """Generate Mermaid ER diagram"""
        lines = ["erDiagram"]
        
        # Add tables
        for table in tables:
            table_name = table["name"]
            lines.append(f"    {table_name} {{")
            
            for column in table["columns"]:
                col_name = column["name"]
                col_type = column.get("type", "VARCHAR")
                nullable = "" if column.get("nullable", True) else " not null"
                pk = " PK" if column.get("primary_key", False) else ""
                lines.append(f"        {col_type} {col_name}{nullable}{pk}")
            
            lines.append("    }")
        
        # Add relationships
        for table in tables:
            if "foreign_keys" in table:
                for fk in table["foreign_keys"]:
                    from_table = table["name"]
                    to_table = fk.get("references_table", "")
                    from_col = fk.get("column", "")
                    to_col = fk.get("references_column", "")
                    
                    if to_table:
                        lines.append(
                            f"    {from_table} ||--o{{ {to_table} : \"{from_col} -> {to_col}\""
                        )
        
        return "\n".join(lines)
    
    def generate_star_schema(self, fact_table: Dict, dim_tables: List[Dict]) -> str:
        """Generate star schema diagram"""
        lines = ["erDiagram"]
        
        # Add fact table
        lines.append(f"    {fact_table['name']} {{")
        for col in fact_table["columns"]:
            lines.append(f"        {col['type']} {col['name']}")
        lines.append("    }")
        
        # Add dimension tables
        for dim in dim_tables:
            lines.append(f"    {dim['name']} {{")
            for col in dim["columns"]:
                lines.append(f"        {col['type']} {col['name']}")
            lines.append("    }")
            
            # Connect to fact table
            lines.append(f"    {dim['name']} ||--o{{ {fact_table['name']} : \"\"")
        
        return "\n".join(lines)


class GraphvizGenerator:
    """Generate Graphviz diagrams"""
    
    def generate_er_diagram(self, tables: List[Dict], style: str = "er") -> str:
        """Generate Graphviz ER diagram"""
        lines = [
            "digraph ER {",
            "    rankdir=LR;",
            "    node [shape=record];"
        ]
        
        # Add tables
        for table in tables:
            table_name = table["name"]
            columns = "|".join([
                f"<{col['name']}> {col['name']}: {col.get('type', 'VARCHAR')}"
                for col in table["columns"]
            ])
            lines.append(f'    {table_name} [label="{{{table_name}|{columns}}}"];')
        
        # Add relationships
        for table in tables:
            if "foreign_keys" in table:
                for fk in table["foreign_keys"]:
                    from_table = table["name"]
                    to_table = fk.get("references_table", "")
                    from_col = fk.get("column", "")
                    to_col = fk.get("references_column", "")
                    
                    if to_table:
                        lines.append(
                            f'    {from_table}:{from_col} -> {to_table}:{to_col} [label="FK"];'
                        )
        
        lines.append("}")
        return "\n".join(lines)
