import React, { useState } from 'react';
import axios from 'axios';

function SchemaDesigner({ onSchemaLoad, schema }) {
  const [database, setDatabase] = useState('');
  const [schemaName, setSchemaName] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const handleReverseEngineer = async () => {
    if (!database || !schemaName) {
      setStatus({ type: 'error', message: 'Please provide database and schema name' });
      return;
    }

    setLoading(true);
    setStatus(null);

    try {
      const response = await axios.get(`/api/snowflake/reverse-engineer`, {
        params: { database, schema: schemaName }
      });
      onSchemaLoad(response.data);
      setStatus({ type: 'success', message: `Loaded ${response.data.tables.length} tables` });
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error.response?.data?.detail || 'Failed to reverse engineer schema' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Reverse Engineer Schema</h2>
      
      {status && (
        <div className={`status ${status.type}`}>
          {status.message}
        </div>
      )}

      <div className="form-group">
        <label>Database:</label>
        <input
          type="text"
          value={database}
          onChange={(e) => setDatabase(e.target.value)}
          placeholder="DB_PROD"
        />
      </div>

      <div className="form-group">
        <label>Schema:</label>
        <input
          type="text"
          value={schemaName}
          onChange={(e) => setSchemaName(e.target.value)}
          placeholder="BRONZE"
        />
      </div>

      <button 
        onClick={handleReverseEngineer} 
        className="primary"
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Reverse Engineer'}
      </button>

      {schema && (
        <div style={{ marginTop: '20px' }}>
          <h3>Schema: {schema.database}.{schema.schema}</h3>
          <p>Tables: {schema.tables.length}</p>
          <ul style={{ textAlign: 'left', listStyle: 'none', padding: 0 }}>
            {schema.tables.map((table, idx) => (
              <li key={idx} style={{ padding: '10px', background: '#f9f9f9', margin: '5px 0', borderRadius: '4px' }}>
                <strong>{table.name}</strong> ({table.columns.length} columns)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default SchemaDesigner;
