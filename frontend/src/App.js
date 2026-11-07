import React, { useState, useEffect } from 'react';

// This 'export default function App()' line is exactly what index.js is looking for!
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
          // Fallback check to ensure we always have an array even if payload_data is named differently
          const dataArray = json.payload_data || json.data || [];
          setTelemetryData(dataArray);
          setNodeStatus({ node_status: json.status || "SUCCESS", venue_node: json.venue_node || "JNNCE_SHIVAMOGGA_INDIA" });
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
    <div style={{ padding: '20px', backgroundColor: '#0b0f19', color: '#ffffff', minHeight: '100vh' }}>
      <h2>🌌 Cosmic Sentinel — Explainer Dashboard</h2>
      <p>Hub Status: <strong style={{ color: '#4ade80' }}>{nodeStatus.node_status}</strong> | Node: <strong>{nodeStatus.venue_node}</strong></p>
      
      {networkError && <div style={{ color: '#ff4d4d', padding: '10px', background: '#221111', borderRadius: '4px', marginBottom: '20px' }}>{networkError}</div>}
      
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px', background: '#111827', borderRadius: '8px', overflow: 'hidden' }}>
        <thead>
          <tr style={{ background: '#1f2937', textAlign: 'left', borderBottom: '2px solid #374151' }}>
            <th style={{ padding: '12px' }}>Object Name</th>
            <th style={{ padding: '12px' }}>Max Diameter (km)</th>
            <th style={{ padding: '12px' }}>Velocity (kph)</th>
            <th style={{ padding: '12px' }}>Hazard State</th>
          </tr>
        </thead>
        <tbody>
          {telemetryData.map((item, index) => {
            // Bulletproof checking for any variations in the data keys
            const isHazard = item.classification === "CRITICAL HAZARD" || item.hazard_state === "CRITICAL HAZARD";
            
            const diameter = item.estimated_diameter_max ?? item.estimated_diameter_max_km ?? 0;
            const velocity = item.relative_velocity ?? item.relative_velocity_kmh ?? 0;
            const statusLabel = item.classification ?? item.hazard_state ?? "UNKNOWN";

            return (
              <tr key={index} style={{ borderBottom: '1px solid #1f2937', background: isHazard ? '#2d1414' : 'transparent' }}>
                <td style={{ padding: '12px' }}>{item.name}</td>
                <td style={{ padding: '12px' }}>
                  {typeof diameter === 'number' ? diameter.toFixed(4) : Number(diameter).toFixed(4)}
                </td>
                <td style={{ padding: '12px' }}>
                  {typeof velocity === 'number' ? velocity.toFixed(2) : Number(velocity).toFixed(2)}
                </td>
                <td style={{ padding: '12px', color: isHazard ? '#ff4d4d' : '#4ade80', fontWeight: 'bold' }}>
                  {statusLabel}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
