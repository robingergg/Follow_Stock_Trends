import React, { useState } from 'react';


function App() {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStockData = async (symbol, timeSeries) => {
    setLoading(true);
    setError(null);
    console.log(`Fetching data for ${symbol} with time series ${timeSeries}`);

    try {
      const url = `http://localhost:8000/stock/${symbol}?time_series=${timeSeries}`;
      console.log('Fetching from:', url);

      
      setStockData(data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}></div>
  );
}

export default App; 