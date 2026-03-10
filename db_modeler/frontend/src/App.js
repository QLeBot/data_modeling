import React, { useState } from 'react';
import './App.css';
import SnowflakeConnection from './components/SnowflakeConnection';
import SchemaDesigner from './components/SchemaDesigner';
import DiagramViewer from './components/DiagramViewer';
import DBTGenerator from './components/DBTGenerator';
import AISchemaGenerator from './components/AISchemaGenerator';

function App() {
  const [connected, setConnected] = useState(false);
  const [schema, setSchema] = useState(null);
  const [activeTab, setActiveTab] = useState('connection');

  return (
    <div className="App">
      <header className="App-header">
        <h1>❄️ DB Modeler - Snowflake Database Modeling Tool</h1>
        <nav>
          <button 
            onClick={() => setActiveTab('connection')}
            className={activeTab === 'connection' ? 'active' : ''}
          >
            Connection
          </button>
          <button 
            onClick={() => setActiveTab('reverse')}
            className={activeTab === 'reverse' ? 'active' : ''}
          >
            Reverse Engineer
          </button>
          <button 
            onClick={() => setActiveTab('ai')}
            className={activeTab === 'ai' ? 'active' : ''}
          >
            AI Design
          </button>
          <button 
            onClick={() => setActiveTab('diagram')}
            className={activeTab === 'diagram' ? 'active' : ''}
          >
            Diagrams
          </button>
          <button 
            onClick={() => setActiveTab('dbt')}
            className={activeTab === 'dbt' ? 'active' : ''}
          >
            dbt Models
          </button>
        </nav>
      </header>

      <main>
        {activeTab === 'connection' && (
          <SnowflakeConnection 
            onConnect={setConnected}
            connected={connected}
          />
        )}
        
        {activeTab === 'reverse' && connected && (
          <SchemaDesigner 
            onSchemaLoad={setSchema}
            schema={schema}
          />
        )}
        
        {activeTab === 'ai' && (
          <AISchemaGenerator 
            onSchemaGenerate={setSchema}
            existingSchema={schema}
          />
        )}
        
        {activeTab === 'diagram' && schema && (
          <DiagramViewer schema={schema} />
        )}
        
        {activeTab === 'dbt' && schema && (
          <DBTGenerator schema={schema} />
        )}
      </main>
    </div>
  );
}

export default App;
