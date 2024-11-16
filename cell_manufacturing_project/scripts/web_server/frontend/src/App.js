// scripts/web_server/frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/data')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading data...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (data.length === 0) {
    return <div>No data available.</div>;
  }

  return (
    <div className="App">
      <h1>Cell Manufacturing Data</h1>
      <table border="1">
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
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.timestamp}</td>
              <td>{row.temperature}</td>
              <td>{row.pressure}</td>
              <td>{row.material_usage}</td>
              <td>{row.process_time}</td>
              <td>{row.defect_rate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;


