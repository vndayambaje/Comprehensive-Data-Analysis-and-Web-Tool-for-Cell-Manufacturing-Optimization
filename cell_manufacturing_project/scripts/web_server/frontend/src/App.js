import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Container, Table, Spinner, Card, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [rawData, setRawData] = useState([]);
  const [processedData, setProcessedData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const rawResponse = await fetch('http://localhost:5000/api/raw_data');
        if (!rawResponse.ok) throw new Error(`HTTP error! Status: ${rawResponse.status}`);
        const rawData = await rawResponse.json();
        setRawData(rawData.slice(0, 5)); // Display only the first 5 entries

        const processedResponse = await fetch('http://localhost:5000/api/processed_data');
        if (!processedResponse.ok) throw new Error(`HTTP error! Status: ${processedResponse.status}`);
        const processedData = await processedResponse.json();
        setProcessedData(processedData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getColorClass = (value, avgValue) => {
    if (!avgValue) return ''; // Return no color if avgValue is not defined or zero
    const diffPercentage = ((value - avgValue) / avgValue) * 100;
    if (diffPercentage > 10 || diffPercentage < -10) {
      return 'red-text';
    } else if (diffPercentage > 5 || diffPercentage < -5) {
      return 'yellow-text';
    } else {
      return 'green-text';
    }
  };

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p>Loading data...</p>
      </Container>
    );
  }

  if (error) {
    return <Container className="text-center text-danger mt-5">Error: {error}</Container>;
  }

  const getAvgForMetric = (metric) => {
    const metricData = processedData.map(d => d[metric]);
    return metricData.length ? metricData.reduce((a, b) => a + b, 0) / metricData.length : null;
  };

  const avgTemperature = getAvgForMetric('avg_temperature');
  const avgPressure = getAvgForMetric('avg_pressure');
  const avgMaterialUsage = getAvgForMetric('avg_material_usage');
  const avgProcessTime = getAvgForMetric('avg_process_time');
  const avgDefectRate = getAvgForMetric('avg_defect_rate');

  return (
    <>
      <div className="sticky-video-container">
        <video autoPlay loop muted className="fullscreen-video">
          <source src="/video.webm" type="video/webm" />
          Your browser does not support the video tag.
        </video>
        <div className="overlay-content">
          <h1>Welcome to the Cell Manufacturing Dashboard</h1>
          <p>Scroll down to view data and analysis.</p>
        </div>
      </div>
      <Container className="mt-4">
        <Row className="mb-4">
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Raw Data (Last 5 Entries)</Card.Title>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Timestamp</th>
                      <th>Stage</th>
                      <th>Temperature</th>
                      <th>Pressure</th>
                      <th>Material Usage</th>
                      <th>Process Time</th>
                      <th>Defect Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rawData.map((row, index) => (
                      <tr key={index}>
                        <td>{row.timestamp}</td>
                        <td>{row.stage}</td>
                        <td className={getColorClass(row.temperature, avgTemperature)}>{row.temperature}</td>
                        <td className={getColorClass(row.pressure, avgPressure)}>{row.pressure}</td>
                        <td className={getColorClass(row.material_usage, avgMaterialUsage)}>{row.material_usage}</td>
                        <td className={getColorClass(row.process_time, avgProcessTime)}>{row.process_time}</td>
                        <td className={getColorClass(row.defect_rate, avgDefectRate)}>{row.defect_rate}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Processed Data - Average Metrics</Card.Title>
                {processedData.length > 0 ? (
                  <div style={{ height: '400px' }}>
                    <Line
                      data={{
                        labels: processedData.map(d => d.stage),
                        datasets: [
                          {
                            label: 'Average Temperature',
                            data: processedData.map(d => d.avg_temperature),
                            fill: false,
                            borderColor: 'rgba(75,192,192,1)',
                            borderWidth: 2,
                            tension: 0.1,
                          },
                          {
                            label: 'Average Pressure',
                            data: processedData.map(d => d.avg_pressure),
                            fill: false,
                            borderColor: 'rgba(153,102,255,1)',
                            borderWidth: 2,
                            tension: 0.1,
                          },
                        ],
                      }}
                      options={{
                        responsive: true,
                        plugins: {
                          legend: { position: 'top' },
                          title: { display: true, text: 'Average Metrics per Stage' },
                        },
                      }}
                    />
                  </div>
                ) : (
                  <div>No processed data available.</div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default App;
