import '../styles/panels.css'

function ClinicalPanel({ data }) {
  if (!data || data.length === 0) {
    return <div className="panel-empty">No clinical trial data available</div>
  }

  const getPhaseColor = (phase) => {
    const phaseMap = {
      'Phase 1': '#e3f2fd',
      'Phase 2': '#f3e5f5',
      'Phase 3': '#fff3e0',
      'Phase 4': '#e8f5e9',
    }
    return phaseMap[phase] || '#f5f5f5'
  }

  return (
    <div className="panel">
      <h3>🧪 Clinical Trials</h3>
      
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Total Trials</h4>
          <p className="metric-value">{data.length}</p>
        </div>
        <div className="summary-card">
          <h4>Phases</h4>
          <p className="metric-value">{new Set(data.map(t => t.phase)).size}</p>
        </div>
      </div>

      <div className="trials-list">
        {data.map((trial, i) => (
          <div 
            key={i} 
            className="trial-card"
            style={{ borderLeftColor: trial.phase?.includes('Phase') ? '#667eea' : '#f57c00' }}
          >
            <div className="trial-header">
              <h4>{trial.title || trial.name || `Trial ${i + 1}`}</h4>
              <span className="trial-phase" style={{ backgroundColor: getPhaseColor(trial.phase) }}>
                {trial.phase || 'Unknown Phase'}
              </span>
            </div>
            
            {trial.trial_id && (
              <p><strong>Trial ID:</strong> {trial.trial_id}</p>
            )}
            
            {trial.status && (
              <p>
                <strong>Status:</strong> 
                <span className={`status-badge status-${trial.status.toLowerCase()}`}>
                  {trial.status}
                </span>
              </p>
            )}
            
            {trial.sponsor && (
              <p><strong>Sponsor:</strong> {trial.sponsor}</p>
            )}
            
            {trial.primary_outcome && (
              <p><strong>Primary Outcome:</strong> {trial.primary_outcome}</p>
            )}
            
            {trial.enrollment && (
              <p><strong>Enrollment:</strong> {trial.enrollment}</p>
            )}
            
            {trial.start_date && (
              <p><strong>Start Date:</strong> {trial.start_date}</p>
            )}
            
            {trial.completion_date && (
              <p><strong>Est. Completion:</strong> {trial.completion_date}</p>
            )}
            
            {trial.description && (
              <div className="trial-description">
                <strong>Description:</strong>
                <p>{trial.description}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ClinicalPanel
