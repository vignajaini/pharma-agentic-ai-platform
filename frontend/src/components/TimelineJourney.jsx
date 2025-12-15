import React from 'react'
import './TimelineJourney.css'

export default function TimelineJourney({ data, molecule }) {
  const stages = [
    {
      number: 1,
      title: 'Molecule Discovery',
      icon: '🔬',
      description: `${molecule} identified for analysis`,
      details: [
        `Molecule: ${molecule}`,
        'Initial assessment complete'
      ]
    },
    {
      number: 2,
      title: 'Unmet Needs Analysis',
      icon: '💡',
      description: 'Identify therapeutic gaps and opportunities',
      details: data.unmet_needs ? [
        `Opportunity Score: ${data.unmet_needs.opportunity_score}/100`,
        `Gaps Identified: ${data.unmet_needs.therapy_gaps?.length || 0}`,
        `Indications: ${data.unmet_needs.indication_opportunities?.length || 0}`
      ] : ['Awaiting analysis']
    },
    {
      number: 3,
      title: 'Clinical Evaluation',
      icon: '🧪',
      description: 'Review ongoing clinical trials',
      details: data.trials ? [
        `Trials Found: ${Array.isArray(data.trials) ? data.trials.length : 0}`,
        'Status: Under clinical development'
      ] : ['No trial data available']
    },
    {
      number: 4,
      title: 'Patent & IP Assessment',
      icon: '📜',
      description: 'Evaluate Freedom to Operate',
      details: data.fto_analysis ? [
        `FTO Risk: ${data.fto_analysis.risk_level}`,
        `Risk Score: ${data.fto_analysis.overall_fto_risk_score}/100`,
        `Patents Found: ${data.fto_analysis.patent_threats?.length || 0}`
      ] : ['Assessment pending']
    },
    {
      number: 5,
      title: 'Innovation Story',
      icon: '⭐',
      description: 'Development of innovative product concept',
      details: [
        `Innovation Score: ${data.mit?.innovation_score || 0}/100`,
        `Market Size: $${data.market?.market_size || 0}M`,
        'Ready for portfolio expansion'
      ]
    }
  ]

  return (
    <div className="timeline-container">
      <h2 className="timeline-title">End-to-End Innovation Journey</h2>
      <div className="timeline">
        {stages.map((stage, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-marker">
              <div className="marker-number">{stage.number}</div>
              <div className="marker-icon">{stage.icon}</div>
            </div>
            
            <div className="timeline-content">
              <h3 className="stage-title">{stage.title}</h3>
              <p className="stage-description">{stage.description}</p>
              <div className="stage-details">
                {stage.details.map((detail, i) => (
                  <div key={i} className="detail-item">
                    <span className="detail-bullet">•</span>
                    <span className="detail-text">{detail}</span>
                  </div>
                ))}
              </div>
            </div>

            {index < stages.length - 1 && (
              <div className="timeline-connector">
                <div className="connector-line"></div>
                <div className="connector-arrow">→</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
