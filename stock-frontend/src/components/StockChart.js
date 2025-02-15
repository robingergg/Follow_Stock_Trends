import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


function StockChart({ data }) {
  if (!data) return <div>No data available</div>;
  const symbol = data["Meta Data"]["2. Symbol"];

  // Convert "Monthly Time Series" to an array so that we can process it further with our chart
  const timeSeries = Object.entries(data["Monthly Time Series"]).map(([date, values]) => ({
    date,
    open: parseFloat(values["1. open"]),
    high: parseFloat(values["2. high"]),
    low: parseFloat(values["3. low"]),
    close: parseFloat(values["4. close"]),
    volume: parseInt(values["5. volume"], 10)
  }));


  return (
    <div style={{ width: '80%', margin: '0 auto' }}>
    </div>
  );
}

export default StockChart; 