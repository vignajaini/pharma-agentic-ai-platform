import '../styles/panels.css'

function PatentPanel({ data }) {
  if (!data || data.length === 0) {
    return <div className="panel-empty">No patent data available</div>
  }

  return (
    <div className="panel">
      <h3>📜 Patents</h3>
      
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Total Patents</h4>
          <p className="metric-value">{data.length}</p>
        </div>
        <div className="summary-card">
          <h4>Patent Families</h4>
          <p className="metric-value">{new Set(data.map(p => p.family_id || p.id)).size}</p>
        </div>
      </div>

      <div className="patents-list">
        {data.map((patent, i) => (
          <div key={i} className="patent-card">
            <div className="patent-header">
              <h4>{patent.title || `Patent ${i + 1}`}</h4>
              <span className="patent-status">
                {patent.status || 'Active'}
              </span>
            </div>
            
            {patent.patent_number && (
              <p><strong>Patent #:</strong> {patent.patent_number}</p>
            )}
            
            {patent.filing_date && (
              <p><strong>Filed:</strong> {patent.filing_date}</p>
            )}
            
            {patent.publication_date && (
              <p><strong>Published:</strong> {patent.publication_date}</p>
            )}
            
            {patent.assignee && (
              <p><strong>Assignee:</strong> {patent.assignee}</p>
            )}
            
            {patent.inventors && (
              <p><strong>Inventors:</strong> {Array.isArray(patent.inventors) ? patent.inventors.join(', ') : patent.inventors}</p>
            )}
            
            {patent.abstract && (
              <div className="patent-abstract">
                <strong>Abstract:</strong>
                <p>{patent.abstract}</p>
              </div>
            )}
            
            {patent.claims && (
              <p><strong>Claims:</strong> {Array.isArray(patent.claims) ? patent.claims.length : 'N/A'}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default PatentPanel
