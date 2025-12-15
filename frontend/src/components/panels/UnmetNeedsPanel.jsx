import React from 'react'
import '../styles/panels.css'

export default function UnmetNeedsPanel({ data }) {
  if (!data) {
    return (
      <div className="panel">
        <p className="empty-message">No unmet needs data available</p>
      </div>
    )
  }

  return (
    <div className="panel">
      <h3 className="panel-title">💡 Unmet Needs Analysis</h3>
      
      <div className="panel-section">
        <h4>Opportunity Score</h4>
        <div className="score-display">
          <div className="score-value">{data.opportunity_score || 0}</div>
          <div className="score-label">/100</div>
        </div>
      </div>

      {data.therapy_gaps && data.therapy_gaps.length > 0 && (
        <div className="panel-section">
          <h4>Therapy Gaps Identified</h4>
          {data.therapy_gaps.map((gap, idx) => (
            <div key={idx} className="info-box">
              <div className="info-title">{gap.gap}</div>
              <p>{gap.description}</p>
              <div className="info-tags">
                <span className="tag">{gap.significance} Significance</span>
                <span className="tag">{gap.potential_impact}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {data.patient_populations && data.patient_populations.length > 0 && (
        <div className="panel-section">
          <h4>Underserved Patient Populations</h4>
          {data.patient_populations.map((pop, idx) => (
            <div key={idx} className="info-box">
              <div className="info-title">{pop.population}</div>
              <p><strong>Current Options:</strong> {pop.current_options}</p>
              <p><strong>Opportunity:</strong> {pop.opportunity}</p>
              <p><strong>Market Potential:</strong> {pop.market_potential}</p>
            </div>
          ))}
        </div>
      )}

      {data.dosage_opportunities && data.dosage_opportunities.length > 0 && (
        <div className="panel-section">
          <h4>Dosage Form Opportunities</h4>
          {data.dosage_opportunities.map((opp, idx) => (
            <div key={idx} className="info-box">
              <div className="info-title">{opp.dosage_form}</div>
              <p><strong>Gap:</strong> {opp.current_gap}</p>
              <p><strong>Regulatory Path:</strong> {opp.regulatory_path}</p>
              <p><strong>Development Time:</strong> {opp.development_time}</p>
            </div>
          ))}
        </div>
      )}

      {data.indication_opportunities && data.indication_opportunities.length > 0 && (
        <div className="panel-section">
          <h4>New Indication Opportunities</h4>
          {data.indication_opportunities.map((ind, idx) => (
            <div key={idx} className="info-box">
              <div className="info-title">{ind.indication}</div>
              <p><strong>Clinical Rationale:</strong> {ind.clinical_rationale}</p>
              <p><strong>Patient Population:</strong> {ind.patient_population}</p>
              <p><strong>Market Opportunity:</strong> {ind.market_opportunity}</p>
              <p><strong>Regulatory Pathway:</strong> {ind.regulatory_pathway}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
