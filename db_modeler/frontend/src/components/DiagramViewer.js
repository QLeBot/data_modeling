import React, { useState, useEffect } from 'react';
import axios from 'axios';
import mermaid from 'mermaid';

function DiagramViewer({ schema }) {
  const [diagram, setDiagram] = useState('');
  const [format, setFormat] = useState('mermaid');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (schema) {
      generateDiagram();
    }
  }, [schema, format]);

  const generateDiagram = async () => {
    if (!schema || !schema.tables) return;

    setLoading(true);

    try {
      // Convert schema to diagram format
      const tables = schema.tables.map(table => ({
        name: table.name,
        columns: table.columns.map(col => ({
          name: col.name || col.COLUMN_NAME,
          type: col.type || col.DATA_TYPE,
          nullable: col.nullable !== false,
          primary_key: false // TODO: detect from schema
        }))
      }));

      const response = await axios.post('/api/diagrams/generate', {
        tables,
        format,
        style: 'er'
      });

      setDiagram(response.data.diagram);
      
      // Render Mermaid diagram
      if (format === 'mermaid') {
        setTimeout(() => {
          mermaid.initialize({ startOnLoad: true, theme: 'default' });
          mermaid.contentLoaded();
        }, 100);
      }
    } catch (error) {
      console.error('Failed to generate diagram:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>ER Diagram</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <label>Format: </label>
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          <option value="mermaid">Mermaid</option>
          <option value="graphviz">Graphviz</option>
        </select>
      </div>

      {loading && <p>Generating diagram...</p>}

      {diagram && (
        <div className="diagram-container">
          {format === 'mermaid' ? (
            <div className="mermaid">{diagram}</div>
          ) : (
            <div className="code-block">
              <pre>{diagram}</pre>
            </div>
          )}
        </div>
      )}

      {!schema && (
        <p>Please reverse engineer a schema or generate one with AI first.</p>
      )}
    </div>
  );
}

export default DiagramViewer;
