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

// TODO: use typescript files for typehinting
function CreateChartData(timeSeries, symbol) {
  const chartData_1 = {
    labels: timeSeries.map(item => item.date), // X-axis labels (dates)
    datasets: [
      {
        label: `Stock Close Price (${symbol})`,
        data: timeSeries.map(item => item.close), // Y-axis values
        borderColor: "blue",
        backgroundColor: "rgba(0, 0, 255, 0.3)",
      }
    ]
  };

  const chartData_2 = {
    labels: timeSeries.map(item => item.date), // X-axis labels (dates)
    datasets: [
      {
        label: `Stock Open Price (${symbol})`,
        data: timeSeries.map(item => item.open), // Y-axis values
        borderColor: "red",
        backgroundColor: "rgba(0, 0, 255, 0.3)",
      }
    ]
  };

  return [chartData_1, chartData_2];
}

function CreateChartOptions(symbol) {
  const options_1 = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Stock Data for ${symbol}`
      }
    }
  };

  const options_2 = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Stock Data for ${symbol}`
      }
    }
  };

  return [options_1, options_2];
}

function StockChart({ data, timeSeriesInd }) {
  if (!data) return <div>No data available</div>;
  const symbol = data["Meta Data"]["2. Symbol"];
  var dataTitle;

  if (timeSeriesInd === "monthly") {
    dataTitle = `Monthly Time Series`;
  } else if (timeSeriesInd === "weekly") {
    dataTitle = `Weekly Time Series`;
  } else if (timeSeriesInd === "daily") {
    dataTitle = `Time Series (Daily)`;
  }

  // Convert "Monthly Time Series" to an array so that we can process it further with our chart
  const timeSeries = Object.entries(data[dataTitle]).map(([date, values]) => ({
    date,
    open: parseFloat(values["1. open"]),
    high: parseFloat(values["2. high"]),
    low: parseFloat(values["3. low"]),
    close: parseFloat(values["4. close"]),
    volume: parseInt(values["5. volume"], 10)
  }));

  // TODO: let high, volume and low to be
  // displayed and let the user open or close the chart
  const [chartData_1, chartData_2] = CreateChartData(timeSeries, symbol);
  const [options_1, options_2] = CreateChartOptions(symbol);

  return (
    <div style={{ width: '80%', margin: '0 auto' }}>
      <Line options={options_1} data={chartData_1} />
      <Line options={options_2} data={chartData_2} />
    </div>
  );
}

export default StockChart; 