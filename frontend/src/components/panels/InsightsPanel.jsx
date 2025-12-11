import '../styles/panels.css'

function InsightsPanel({ data }) {
  if (!data) {
    return <div className="panel-empty">No internal insights available</div>
  }

  return (
    <div className="panel">
      <h3>📚 Internal Insights</h3>
      
      {typeof data === 'string' ? (
        <div className="data-card full-width">
          <p>{data}</p>
        </div>
      ) : Array.isArray(data) ? (
        <div className="insights-list">
          {data.map((insight, i) => (
            <div key={i} className="insight-card">
              <h4>{insight.title || insight.name || `Insight ${i + 1}`}</h4>
              <p>{insight.description || insight.content || insight}</p>
              {insight.category && (
                <span className="insight-category">{insight.category}</span>
              )}
              {insight.date && (
                <span className="insight-date">{insight.date}</span>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="data-card full-width">
          {Object.entries(data).map(([key, value]) => (
            <div key={key} className="insight-item">
              <h4>{key}</h4>
              <p>{typeof value === 'object' ? JSON.stringify(value) : value}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default InsightsPanel
