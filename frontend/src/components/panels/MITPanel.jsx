import '../styles/panels.css'

function MITPanel({ data, molecule }) {
  if (!data) {
    return <div className="panel-empty">No MIT data available</div>
  }

  const mitData = typeof data === 'string' ? JSON.parse(data) : data

  return (
    <div className="panel">
      <h3>💡 Molecule Innovation Twin (MIT)</h3>
      
      {mitData.innovation_score !== undefined && (
        <div className="metric-card">
          <h4>Innovation Score</h4>
          <div className="score-display">
            <div className="score-value">{mitData.innovation_score?.toFixed(2) || 'N/A'}</div>
            <div className="score-bar">
              <div 
                className="score-fill" 
                style={{ width: `${Math.min((mitData.innovation_score || 0) * 10, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}

      <div className="grid-2">
        {mitData.market_potential && (
          <div className="data-card">
            <h4>📊 Market Potential</h4>
            <p>{mitData.market_potential}</p>
          </div>
        )}
        
        {mitData.research_status && (
          <div className="data-card">
            <h4>🧪 Research Status</h4>
            <p>{mitData.research_status}</p>
          </div>
        )}
      </div>

      {mitData.summary && (
        <div className="data-card full-width">
          <h4>Summary</h4>
          <p>{mitData.summary}</p>
        </div>
      )}

      {mitData.recommendations && (
        <div className="data-card full-width">
          <h4>🎯 Recommendations</h4>
          <ul className="data-list">
            {Array.isArray(mitData.recommendations) ? (
              mitData.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))
            ) : (
              <li>{mitData.recommendations}</li>
            )}
          </ul>
        </div>
      )}

      {mitData.key_metrics && (
        <div className="data-card full-width">
          <h4>📈 Key Metrics</h4>
          <div className="metrics-grid">
            {Object.entries(mitData.key_metrics).map(([key, value]) => (
              <div key={key} className="metric-item">
                <span className="metric-label">{key}:</span>
                <span className="metric-value">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default MITPanel
