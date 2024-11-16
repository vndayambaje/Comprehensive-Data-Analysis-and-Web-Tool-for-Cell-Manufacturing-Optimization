// src/App.js
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/data');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const fetchedData = await response.json();
        setData(fetchedData);

        if (fetchedData && fetchedData.length > 0) {
          const timestamps = fetchedData.map(d => d.timestamp);
          const temperatures = fetchedData.map(d => d.temperature);

          setChartData({
            labels: timestamps,
            datasets: [
              {
                label: 'Temperature Over Time',
                data: temperatures,
                fill: false,
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 2,
                tension: 0.1,
              },
            ],
          });
        } else {
          setChartData({
            labels: [],
            datasets: [],
          });
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading data...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="App">
      <div className="video-container">
        <video className="fullscreen-video" autoPlay loop muted playsInline>
          <source src="/video.webm" type="video/webm" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className="content">
        <h1>Cell Manufacturing Dashboard</h1>

        {chartData && chartData.labels.length > 0 ? (
          <div className="chart-container">
            <Line data={chartData} options={{ maintainAspectRatio: false }} />
          </div>
        ) : (
          <div>No chart data available.</div>
        )}

        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Temperature</th>
              <th>Pressure</th>
              <th>Material Usage</th>
              <th>Process Time</th>
              <th>Defect Rate</th>
            </tr>
          </thead>
          <tbody>
            {data.length > 0 ? (
              data.map((row, index) => (
                <tr key={index}>
                  <td>{row.timestamp}</td>
                  <td>{row.temperature}</td>
                  <td>{row.pressure}</td>
                  <td>{row.material_usage}</td>
                  <td>{row.process_time}</td>
                  <td>{row.defect_rate}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">No data available</td>
              </tr>
            )}
          </tbody>
        </table>

        <div className="chat-box">
          <h2>Chat</h2>
          {/* Chat logic goes here */}
        </div>
      </div>
    </div>
  );
}

export default App;
