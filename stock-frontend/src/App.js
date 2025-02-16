import React, { useState } from 'react';
import StockChart from './components/StockChart';
import StockForm from './components/StockForm';

function App() {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timeSeriesInd, setTimeSeriesInd] = useState(null);

  const fetchStockData = async (symbol, timeSeries, useMock) => {
    setLoading(true);
    setError(null);
    console.log(`Fetching data for ${symbol} with time series ${timeSeries}`);

    console.log(`Using mock data: ${useMock}`);

    if (!symbol) {
      setError('Symbol is required, eg. IBM');
      setLoading(false);
      return;
    }
    

    try {
      const url = `http://localhost:8000/stock/${symbol}?time_series=${timeSeries}&use_mock=${useMock}`;
      console.log('Fetching from:', url);
      
      const response = await fetch(url);
      console.log('Response:', response);
      
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      console.log('Received data:', data);

      Object.entries(data).forEach(([k, v]) => console.log(k, v))
      
      setStockData(data);
      setTimeSeriesInd(timeSeries);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Stock Data Visualization - DMLAB</h1>
      <StockForm onSubmit={fetchStockData} />
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {stockData && <StockChart data={stockData} timeSeriesInd={timeSeriesInd} />}
    </div>
  );
}

export default App; 