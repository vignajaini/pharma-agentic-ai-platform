import '../styles/panels.css'

function WebPanel({ data }) {
  if (!data || data.length === 0) {
    return <div className="panel-empty">No web research data available</div>
  }

  return (
    <div className="panel">
      <h3>🌐 Web Research Results</h3>
      
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Articles Found</h4>
          <p className="metric-value">{data.length}</p>
        </div>
      </div>

      <div className="web-results-list">
        {data.map((result, i) => (
          <div key={i} className="web-result-card">
            <div className="result-header">
              <h4>
                {result.url ? (
                  <a href={result.url} target="_blank" rel="noopener noreferrer">
                    {result.title || 'Untitled Article'}
                  </a>
                ) : (
                  result.title || 'Untitled Article'
                )}
              </h4>
              <span className="result-source">{result.source || 'Unknown Source'}</span>
            </div>
            
            {result.description && (
              <p className="result-description">{result.description}</p>
            )}
            
            {result.snippet && (
              <p className="result-snippet">{result.snippet}</p>
            )}
            
            <div className="result-meta">
              {result.date && (
                <span className="meta-item">📅 {result.date}</span>
              )}
              {result.relevance && (
                <span className="meta-item">
                  ⭐ Relevance: {result.relevance}
                </span>
              )}
            </div>
            
            {result.url && (
              <p className="result-url">
                <a href={result.url} target="_blank" rel="noopener noreferrer">
                  Read More →
                </a>
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default WebPanel
