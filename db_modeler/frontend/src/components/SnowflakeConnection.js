import React, { useState } from 'react';
import axios from 'axios';

function SnowflakeConnection({ onConnect, connected }) {
  const [formData, setFormData] = useState({
    account: '',
    user: '',
    password: '',
    warehouse: '',
    database: '',
    schema: ''
  });
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleConnect = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);

    try {
      const response = await axios.post('/api/snowflake/connect', formData);
      setStatus({ type: 'success', message: `Connected! Snowflake version: ${response.data.snowflake_version}` });
      onConnect(true);
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error.response?.data?.detail || 'Connection failed' 
      });
      onConnect(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Snowflake Connection</h2>
      {status && (
        <div className={`status ${status.type}`}>
          {status.message}
        </div>
      )}
      
      <form onSubmit={handleConnect}>
        <div className="form-group">
          <label>Account:</label>
          <input
            type="text"
            name="account"
            value={formData.account}
            onChange={handleChange}
            required
            placeholder="your_account.snowflakecomputing.com"
          />
        </div>

        <div className="form-group">
          <label>User:</label>
          <input
            type="text"
            name="user"
            value={formData.user}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Warehouse:</label>
          <input
            type="text"
            name="warehouse"
            value={formData.warehouse}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Database:</label>
          <input
            type="text"
            name="database"
            value={formData.database}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Schema:</label>
          <input
            type="text"
            name="schema"
            value={formData.schema}
            onChange={handleChange}
          />
        </div>

        <button type="submit" className="primary" disabled={loading}>
          {loading ? 'Connecting...' : 'Connect to Snowflake'}
        </button>
      </form>
    </div>
  );
}

export default SnowflakeConnection;
