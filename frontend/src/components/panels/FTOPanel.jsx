import React from 'react'
import '../styles/panels.css'

export default function FTOPanel({ data }) {
  if (!data) {
    return (
      <div className="panel">
        <p className="empty-message">No FTO data available</p>
      </div>
    )
  }

  const getRiskColor = (level) => {
    switch(level) {
      case 'HIGH':
        return '#ef4444'
      case 'MEDIUM':
        return '#f59e0b'
      case 'LOW':
        return '#10b981'
      default:
        return '#6b7280'
    }
  }

  return (
    <div className="panel">
      <h3 className="panel-title">📜 FTO Risk Assessment</h3>
      
      <div className="panel-section">
        <h4>Overall FTO Risk</h4>
        <div style={{
          background: getRiskColor(data.risk_level),
          color: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          textAlign: 'center',
          marginBottom: '1rem'
        }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {data.overall_fto_risk_score}/100
          </div>
          <div style={{ fontSize: '1.1rem', marginTop: '0.5rem' }}>
            {data.risk_level} RISK
          </div>
        </div>
      </div>

      {data.patent_threats && data.patent_threats.length > 0 && (
        <div className="panel-section">
          <h4>Active Patent Threats ({data.patent_threats.length})</h4>
          {data.patent_threats.map((threat, idx) => (
            <div key={idx} className="info-box" style={{
              borderLeft: `4px solid ${threat.threat_severity === 'HIGH' ? '#ef4444' : '#f59e0b'}`
            }}>
              <div className="info-title">{threat.patent_id}</div>
              <p><strong>Owner:</strong> {threat.owner}</p>
              <p><strong>Expiry:</strong> {threat.expiry_date}</p>
              <p><strong>Years Remaining:</strong> {threat.years_remaining}</p>
              <p><strong>Severity:</strong> {threat.threat_severity}</p>
              <p><strong>Claims:</strong> {threat.claims_count}</p>
              <p><strong>Risk Overlap:</strong> {threat.risk_overlap}</p>
            </div>
          ))}
        </div>
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <div className="panel-section">
          <h4>Recommendations</h4>
          <ul style={{ paddingLeft: '1.5rem' }}>
            {data.recommendations.map((rec, idx) => (
              <li key={idx} style={{ marginBottom: '0.75rem', lineHeight: '1.6' }}>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="panel-section">
        <h4>Expiry Timeline</h4>
        {data.expiry_timeline && (
          <>
            {data.expiry_timeline.near_term && data.expiry_timeline.near_term.length > 0 && (
              <div>
                <h5 style={{ color: '#ef4444', marginTop: '0.75rem' }}>Near Term (0-3 years)</h5>
                {data.expiry_timeline.near_term.map((p, idx) => (
                  <p key={idx} style={{ fontSize: '0.9rem', color: '#666' }}>
                    {p.patent_id}: {p.expiry_date}
                  </p>
                ))}
              </div>
            )}
            {data.expiry_timeline.medium_term && data.expiry_timeline.medium_term.length > 0 && (
              <div>
                <h5 style={{ color: '#f59e0b', marginTop: '0.75rem' }}>Medium Term (3-7 years)</h5>
                {data.expiry_timeline.medium_term.map((p, idx) => (
                  <p key={idx} style={{ fontSize: '0.9rem', color: '#666' }}>
                    {p.patent_id}: {p.expiry_date}
                  </p>
                ))}
              </div>
            )}
            {data.expiry_timeline.long_term && data.expiry_timeline.long_term.length > 0 && (
              <div>
                <h5 style={{ color: '#10b981', marginTop: '0.75rem' }}>Long Term (7+ years)</h5>
                {data.expiry_timeline.long_term.map((p, idx) => (
                  <p key={idx} style={{ fontSize: '0.9rem', color: '#666' }}>
                    {p.patent_id}: {p.expiry_date}
                  </p>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
