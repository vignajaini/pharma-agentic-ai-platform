import { useState } from 'react'
import './ResultsDisplay.css'
import MarketPanel from './panels/MarketPanel'
import TradePanel from './panels/TradePanel'
import PatentPanel from './panels/PatentPanel'
import ClinicalPanel from './panels/ClinicalPanel'
import WebPanel from './panels/WebPanel'
import InsightsPanel from './panels/InsightsPanel'
import MITPanel from './panels/MITPanel'
import UnmetNeedsPanel from './panels/UnmetNeedsPanel'
import FTOPanel from './panels/FTOPanel'
import ChartDisplay from './ChartDisplay'
import TimelineJourney from './TimelineJourney'

function ResultsDisplay({ results, onDownloadReport }) {
  const [activeTab, setActiveTab] = useState('journey')

  const tabs = [
    { id: 'journey', label: '🚀 Journey', icon: '🚀' },
    { id: 'charts', label: '📈 Charts', icon: '📈' },
    { id: 'mit', label: '💡 MIT', icon: '💡' },
    { id: 'unmet', label: '💡 Unmet Needs', icon: '💡' },
    { id: 'fto', label: '⚖️ FTO Risk', icon: '⚖️' },
    { id: 'market', label: '📊 Market', icon: '📊' },
    { id: 'trade', label: '🌍 Trade', icon: '🌍' },
    { id: 'patents', label: '📜 Patents', icon: '📜' },
    { id: 'trials', label: '🧪 Clinical', icon: '🧪' },
    { id: 'web', label: '🌐 Web', icon: '🌐' },
    { id: 'internal', label: '📚 Insights', icon: '📚' },
  ]

  return (
    <div className="results-container">
      <div className="results-header">
        <div className="molecule-info">
          <h2>Molecule: <span className="molecule-name">{results.molecule}</span></h2>
          <p className="timestamp">Analysis completed {new Date().toLocaleTimeString()}</p>
        </div>
        <button className="download-btn" onClick={onDownloadReport}>
          📥 Download PDF Report
        </button>
      </div>

      <div className="tabs-container">
        <div className="tabs-list">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              title={tab.label}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="results-content">
        {activeTab === 'journey' && (
          <TimelineJourney data={results} molecule={results.molecule} />
        )}
        {activeTab === 'charts' && (
          <ChartDisplay data={results} />
        )}
        {activeTab === 'mit' && (
          <MITPanel data={results.mit} molecule={results.molecule} />
        )}
        {activeTab === 'unmet' && (
          <UnmetNeedsPanel data={results.unmet_needs} />
        )}
        {activeTab === 'fto' && (
          <FTOPanel data={results.fto_analysis} />
        )}
        {activeTab === 'market' && (
          <MarketPanel data={results.market} />
        )}
        {activeTab === 'trade' && (
          <TradePanel data={results.trade} />
        )}
        {activeTab === 'patents' && (
          <PatentPanel data={results.patents} />
        )}
        {activeTab === 'trials' && (
          <ClinicalPanel data={results.trials} />
        )}
        {activeTab === 'web' && (
          <WebPanel data={results.web} />
        )}
        {activeTab === 'internal' && (
          <InsightsPanel data={results.internal} />
        )}
      </div>
    </div>
  )
}

export default ResultsDisplay
