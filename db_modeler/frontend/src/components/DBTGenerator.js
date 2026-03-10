import React, { useState } from 'react';
import axios from 'axios';

function DBTGenerator({ schema }) {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);

  const handleGenerate = async () => {
    if (!schema) {
      alert('Please load a schema first');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('/api/dbt/generate-models', {
        database: schema.database,
        schema: schema.schema,
        model_type: 'view'
      });

      setModels(response.data.models);
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to generate dbt models');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (models.length === 0) {
      alert('No models to export');
      return;
    }

    try {
      const response = await axios.post('/api/dbt/export', {
        models: models.map(m => ({ name: m.name, code: m.code })),
        output_path: './dbt/models/generated'
      });

      alert(`Exported ${response.data.count} models`);
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to export models');
    }
  };

  return (
    <div className="card">
      <h2>dbt Model Generator</h2>
      
      {schema && (
        <div>
          <p>Schema: {schema.database}.{schema.schema}</p>
          <button onClick={handleGenerate} className="primary" disabled={loading}>
            {loading ? 'Generating...' : 'Generate dbt Models'}
          </button>
        </div>
      )}

      {models.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3>Generated Models ({models.length})</h3>
          <button onClick={handleExport} className="secondary">
            Export All Models
          </button>

          <div style={{ marginTop: '15px' }}>
            {models.map((model, idx) => (
              <div key={idx} style={{ marginBottom: '15px', textAlign: 'left' }}>
                <button 
                  onClick={() => setSelectedModel(selectedModel === idx ? null : idx)}
                  style={{ 
                    background: '#667eea', 
                    color: 'white', 
                    border: 'none', 
                    padding: '8px 15px',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  {model.name}
                </button>
                
                {selectedModel === idx && (
                  <div className="code-block" style={{ marginTop: '10px' }}>
                    <pre>{model.code}</pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {!schema && (
        <p>Please load a schema first to generate dbt models.</p>
      )}
    </div>
  );
}

export default DBTGenerator;
