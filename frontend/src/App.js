import React, { useState, useEffect } from 'react';

export default function App() {
  const [telemetryData, setTelemetryData] = useState([]);
  const [nodeStatus, setNodeStatus] = useState({ node_status: "WAITING_CONNECTION", venue_node: "JNNCE_SHIVAMOGGA_INDIA" });
  const [networkError, setNetworkError] = useState(null);

  useEffect(() => {
    const fetchTelemetryPayload = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/telemetry');
        if (response.ok) {
          const json = await response.json();
          setTelemetryData(json.payload_data);
          setNodeStatus({ node_status: json.status, venue_node: json.venue_node });
        } else {
          setNetworkError(`HTTP Node Failure: ${response.status}`);
        }
      } catch (err) {
        setNetworkError(`Offline: ${err.message}`);
      }
    };
    fetchTelemetryPayload();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>🌌 Cosmic Sentinel — Explainer Dashboard</h2>
      <p>Hub Status: <strong>{nodeStatus.node_status}</strong> | Node: <strong>{nodeStatus.venue_node}</strong></p>
      
      {networkError && <div style={{ color: '#ff4d4d', padding: '10px', background: '#221111', borderRadius: '4px' }}>{networkError}</div>}
      
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr style={{ background: '#111827', textAlign: 'left', borderBottom: '2px solid #374151' }}>
            <th style={{ padding: '12px' }}>Object Name</th>
            <th style={{ padding: '12px' }}>Max Diameter (km)</th>
            <th style={{ padding: '12px' }}>Velocity (kph)</th>
            <th style={{ padding: '12px' }}>Hazard State</th>
          </tr>
        </thead>
        <tbody>
          {telemetryData.map((item, index) => {
            const isHazard = item.classification === "CRITICAL HAZARD";
            return (
              <tr key={index} style={{ borderBottom: '1px solid #1f2937', background: isHazard ? '#2d1414' : 'transparent' }}>
                <td style={{ padding: '12px' }}>{item.name}</td>
                <td style={{ padding: '12px' }}>{item.estimated_diameter_max.toFixed(4)}</td>
                <td style={{ padding: '12px' }}>{item.relative_velocity.toFixed(2)}</td>
                <td style={{ padding: '12px', color: isHazard ? '#ff4d4d' : '#4ade80', fontWeight: 'bold' }}>{item.classification}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
