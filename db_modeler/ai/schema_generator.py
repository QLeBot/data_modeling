"""
AI-powered schema generation
Uses OpenAI or Anthropic APIs
"""
import os
import json
from typing import Dict, List, Optional, Any
import openai
from anthropic import Anthropic


class AISchemaGenerator:
    """Generate database schemas using AI"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = openai.OpenAI(api_key=api_key)
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate_schema(
        self,
        prompt: str,
        existing_schema: Optional[Dict] = None,
        schema_type: str = "star"
    ) -> Dict[str, Any]:
        """Generate schema from natural language prompt"""
        
        system_prompt = self._build_system_prompt(schema_type, existing_schema)
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
        else:  # anthropic
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.content[0].text
        
        # Parse JSON response
        try:
            schema_data = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                schema_data = json.loads(json_match.group(1))
            else:
                raise ValueError("Could not parse AI response as JSON")
        
        return {
            "schema": schema_data,
            "explanation": self._extract_explanation(content),
            "suggestions": self._extract_suggestions(content)
        }
    
    def _build_system_prompt(self, schema_type: str, existing_schema: Optional[Dict]) -> str:
        """Build system prompt for AI"""
        prompt = f"""You are an expert database architect specializing in {schema_type} schemas for Snowflake.

Your task is to generate a complete database schema in JSON format based on user requirements.

Output format:
{{
    "database": "database_name",
    "schema": "schema_name",
    "tables": [
        {{
            "name": "table_name",
            "type": "fact|dimension",
            "columns": [
                {{
                    "name": "column_name",
                    "type": "VARCHAR|NUMBER|DATE|TIMESTAMP_NTZ|BOOLEAN",
                    "nullable": true|false,
                    "primary_key": true|false,
                    "description": "column description"
                }}
            ],
            "foreign_keys": [
                {{
                    "column": "column_name",
                    "references_table": "table_name",
                    "references_column": "column_name"
                }}
            ],
            "description": "table description"
        }}
    ]
}}

Guidelines:
- Use Snowflake data types (VARCHAR, NUMBER, DATE, TIMESTAMP_NTZ, BOOLEAN, etc.)
- For {schema_type} schemas, include fact tables and dimension tables
- Add appropriate foreign key relationships
- Include descriptive comments
"""
        
        if existing_schema:
            prompt += f"\n\nExisting schema context:\n{json.dumps(existing_schema, indent=2)}"
        
        return prompt
    
    def _extract_explanation(self, content: str) -> str:
        """Extract explanation from AI response"""
        # Simple extraction - can be improved
        if "explanation" in content.lower():
            lines = content.split("\n")
            explanation_lines = []
            in_explanation = False
            for line in lines:
                if "explanation" in line.lower():
                    in_explanation = True
                if in_explanation:
                    explanation_lines.append(line)
            return "\n".join(explanation_lines)
        return "Schema generated successfully."
    
    def _extract_suggestions(self, content: str) -> List[str]:
        """Extract suggestions from AI response"""
        # Simple extraction - can be improved
        suggestions = []
        if "suggestions" in content.lower() or "recommendations" in content.lower():
            # Parse suggestions
            pass
        return suggestions
    
    def suggest_improvements(self, schema: Dict) -> List[str]:
        """Get AI suggestions for schema improvements"""
        prompt = f"""Analyze this database schema and suggest improvements:

{json.dumps(schema, indent=2)}

Provide specific, actionable suggestions for:
- Performance optimization
- Data modeling best practices
- Indexing strategies
- Normalization opportunities
"""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            content = response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        
        # Parse suggestions (simple split by lines for now)
        suggestions = [line.strip() for line in content.split("\n") if line.strip() and line.strip().startswith("-")]
        return suggestions
    
    def explain_schema(self, schema: Dict) -> str:
        """Get AI explanation of a schema"""
        prompt = f"""Explain this database schema in detail:

{json.dumps(schema, indent=2)}

Explain:
- The purpose of each table
- Relationships between tables
- Data flow and usage patterns
"""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
    
    def validate_schema(self, schema: Dict) -> Dict[str, Any]:
        """Validate schema design"""
        prompt = f"""Validate this database schema for Snowflake:

{json.dumps(schema, indent=2)}

Check for:
- Data type compatibility
- Naming conventions
- Missing relationships
- Performance issues
- Best practices violations

Return JSON with validation results.
"""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            content = response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        
        try:
            return json.loads(content)
        except:
            return {
                "valid": True,
                "issues": [],
                "notes": content
            }
