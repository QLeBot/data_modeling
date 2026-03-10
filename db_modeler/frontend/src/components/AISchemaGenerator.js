import React, { useState } from 'react';
import axios from 'axios';

function AISchemaGenerator({ onSchemaGenerate, existingSchema }) {
  const [prompt, setPrompt] = useState('');
  const [schemaType, setSchemaType] = useState('star');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert('Please enter a description');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('/api/ai/generate-schema', {
        prompt,
        existing_schema: existingSchema,
        schema_type: schemaType,
        provider: 'openai'
      });
      
      setResult(response.data);
      onSchemaGenerate(response.data.schema);
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to generate schema');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>AI Schema Generator</h2>
      <p>Describe your database schema in natural language and let AI design it for you.</p>

      <div className="form-group">
        <label>Schema Type:</label>
        <select value={schemaType} onChange={(e) => setSchemaType(e.target.value)}>
          <option value="star">Star Schema</option>
          <option value="snowflake">Snowflake Schema</option>
          <option value="normalized">Normalized</option>
        </select>
      </div>

      <div className="form-group">
        <label>Describe your schema:</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows="6"
          placeholder="Example: I need a sales data warehouse with a fact table for sales transactions and dimension tables for customers, products, dates, and stores..."
        />
      </div>

      <button onClick={handleGenerate} className="primary" disabled={loading}>
        {loading ? 'Generating...' : 'Generate Schema with AI'}
      </button>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Generated Schema</h3>
          <div className="code-block">
            <pre>{JSON.stringify(result.schema, null, 2)}</pre>
          </div>
          
          {result.explanation && (
            <div style={{ marginTop: '15px', textAlign: 'left' }}>
              <h4>Explanation:</h4>
              <p>{result.explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AISchemaGenerator;
