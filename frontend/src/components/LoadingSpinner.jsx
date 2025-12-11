import './LoadingSpinner.css'

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner-wrapper">
        <div className="spinner"></div>
        <h2>Analyzing Molecule</h2>
        <p>Gathering data from all agents...</p>
        <div className="loading-stages">
          <div className="stage">
            <span className="stage-icon">📊</span>
            <span>Market Data</span>
          </div>
          <div className="stage">
            <span className="stage-icon">🌍</span>
            <span>Trade Data</span>
          </div>
          <div className="stage">
            <span className="stage-icon">📜</span>
            <span>Patents</span>
          </div>
          <div className="stage">
            <span className="stage-icon">🧪</span>
            <span>Clinical</span>
          </div>
          <div className="stage">
            <span className="stage-icon">🌐</span>
            <span>Web</span>
          </div>
          <div className="stage">
            <span className="stage-icon">📚</span>
            <span>Insights</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoadingSpinner
