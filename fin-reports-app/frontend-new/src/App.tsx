import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface PriceData {
  date: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number | null;
}

interface ReportData {
  asset: string;
  asset_name: string;
  from: string;
  to: string;
  data: PriceData[];
  count: number;
}

interface Asset {
  symbol: string;
  name: string;
}

function App() {
  const [asset, setAsset] = useState("TSLA");
  const [fromDate, setFromDate] = useState("2025-07-01");
  const [toDate, setToDate] = useState("2025-08-10");
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = "http://localhost:8000";

  // Load available assets on component mount
  useEffect(() => {
    const loadAssets = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/assets`);
        setAssets(response.data);
      } catch (err) {
        console.error("Error loading assets:", err);
        setError("Failed to load available assets");
      }
    };
    loadAssets();
  }, []);

  const fetchReport = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API_BASE_URL}/reports`, {
        params: { 
          asset: asset, 
          from_date: fromDate, 
          to_date: toDate 
        },
        headers: { 
          Authorization: "Bearer fake-token" 
        }
      });
      setReportData(response.data);
    } catch (err: any) {
      console.error("Error fetching report:", err);
      setError(err.response?.data?.detail || "Failed to fetch report data");
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data
  const chartData = reportData ? {
    labels: reportData.data.map(item => item.date),
    datasets: [
      {
        label: 'Close Price',
        data: reportData.data.map(item => item.close),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
      {
        label: 'High Price',
        data: reportData.data.map(item => item.high),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1,
        borderDash: [5, 5],
      },
      {
        label: 'Low Price',
        data: reportData.data.map(item => item.low),
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.1,
        borderDash: [5, 5],
      }
    ],
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: reportData ? `${reportData.asset_name} (${reportData.asset}) Price Chart` : 'Financial Data',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Price (USD)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    },
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📈 Financial Reports Dashboard</h1>
        <p>Advanced financial data visualization and analysis</p>
      </header>

      <main className="main-content">
        <div className="controls-section">
          <h2>🔍 Search Financial Data</h2>
          
          <div className="form-group">
            <label htmlFor="asset-select">Asset:</label>
            <select 
              id="asset-select"
              value={asset} 
              onChange={e => setAsset(e.target.value)}
              className="form-control"
            >
              {assets.map(assetItem => (
                <option key={assetItem.symbol} value={assetItem.symbol}>
                  {assetItem.symbol} - {assetItem.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="from-date">From Date:</label>
            <input 
              id="from-date"
              type="date" 
              value={fromDate} 
              onChange={e => setFromDate(e.target.value)}
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label htmlFor="to-date">To Date:</label>
            <input 
              id="to-date"
              type="date" 
              value={toDate} 
              onChange={e => setToDate(e.target.value)}
              className="form-control"
            />
          </div>

          <button 
            onClick={fetchReport} 
            disabled={loading}
            className="search-button"
          >
            {loading ? "⏳ Loading..." : "📊 Generate Report"}
          </button>
        </div>

        {error && (
          <div className="error-message">
            ❌ Error: {error}
          </div>
        )}

        {reportData && chartData && (
          <div className="results-section">
            <h2>📊 Price Chart for {reportData.asset_name}</h2>
            <div className="chart-info">
              <p><strong>Symbol:</strong> {reportData.asset}</p>
              <p><strong>Period:</strong> {reportData.from} to {reportData.to}</p>
              <p><strong>Data Points:</strong> {reportData.count}</p>
            </div>
            
            <div className="chart-container">
              <Line data={chartData} options={chartOptions} />
            </div>

            <div className="data-summary">
              <h3>📈 Data Summary</h3>
              {reportData.data.length > 0 && (
                <div className="summary-stats">
                  <div className="stat-card">
                    <h4>Latest Price</h4>
                    <p>${reportData.data[reportData.data.length - 1]?.close?.toFixed(2)}</p>
                  </div>
                  <div className="stat-card">
                    <h4>Highest Price</h4>
                    <p>${Math.max(...reportData.data.map(d => d.high || 0)).toFixed(2)}</p>
                  </div>
                  <div className="stat-card">
                    <h4>Lowest Price</h4>
                    <p>${Math.min(...reportData.data.map(d => d.low || Infinity)).toFixed(2)}</p>
                  </div>
                  <div className="stat-card">
                    <h4>Avg Volume</h4>
                    <p>{Math.round(reportData.data.reduce((sum, d) => sum + (d.volume || 0), 0) / reportData.data.length).toLocaleString()}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
