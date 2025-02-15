import React, { useState } from 'react';

function StockForm({ onSubmit }) {
  const [symbol, setSymbol] = useState('');
  const [timeSeries, setTimeSeries] = useState('monthly');
  const [useMock, setUseMock] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(symbol, timeSeries, useMock);
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Enter stock symbol (e.g., IBM)"
          style={{ margin: '0 10px', padding: '5px' }}
        />
        <select
          value={timeSeries}
          onChange={(e) => setTimeSeries(e.target.value)}
          style={{ margin: '0 10px', padding: '5px' }}
        >
          <option value="monthly">Monthly</option>
          <option value="weekly">Weekly</option>
          <option value="daily">Daily</option>
        </select>

        {/* Checkbox for Mock Data */}
        <label style={{ marginLeft: '10px' }}>
          <input
            type="checkbox"
            checked={useMock}
            onChange={(e) => setUseMock(e.target.checked)}
            style={{ marginRight: '5px' }}
          />
          Use Mock Data
        </label>
        <button type="submit" style={{ padding: '5px 10px' }}>Get Data</button>
      </form>
    </div>
  );
}

export default StockForm; 