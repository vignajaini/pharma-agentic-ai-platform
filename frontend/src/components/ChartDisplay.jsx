import React from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement } from 'chart.js'
import { Pie, Bar, Line } from 'react-chartjs-2'
import './ChartDisplay.css'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement)

export default function ChartDisplay({ data, chartType = 'pie' }) {
  if (!data) return null

  // Innovation Score Chart
  const renderInnovationChart = () => {
    const score = data.mit?.innovation_score || 0
    const chartData = {
      labels: ['Innovation Score', 'Remaining'],
      datasets: [
        {
          data: [score, 100 - score],
          backgroundColor: ['#3b82f6', '#e5e7eb'],
          borderColor: ['#1e40af', '#d1d5db'],
          borderWidth: 2,
        },
      ],
    }
    return (
      <div className="chart-container">
        <h3>Innovation Score</h3>
        <Pie data={chartData} options={{ maintainAspectRatio: true }} />
        <p className="chart-label">{score.toFixed(1)}/100</p>
      </div>
    )
  }

  // Market Data Chart
  const renderMarketChart = () => {
    if (!data.market || typeof data.market !== 'object') return null
    
    const marketSize = data.market.market_size || 0
    const growth = data.market.cagr || 0
    
    const chartData = {
      labels: ['Current Market', 'Projected Growth'],
      datasets: [
        {
          label: 'Market Value ($M)',
          data: [marketSize, marketSize * (1 + growth / 100)],
          backgroundColor: ['#10b981', '#34d399'],
          borderColor: ['#059669', '#10b981'],
          borderWidth: 2,
        },
      ],
    }
    
    return (
      <div className="chart-container">
        <h3>Market Analysis</h3>
        <Bar data={chartData} options={{ maintainAspectRatio: true }} />
      </div>
    )
  }

  // FTO Risk Chart
  const renderFTOChart = () => {
    if (!data.fto_analysis) return null
    
    const riskScore = data.fto_analysis.overall_fto_risk_score || 0
    const riskLevel = data.fto_analysis.risk_level || 'UNKNOWN'
    
    const riskColor = 
      riskLevel === 'HIGH' ? '#ef4444' :
      riskLevel === 'MEDIUM' ? '#f59e0b' :
      '#10b981'
    
    const chartData = {
      labels: ['Risk Level', 'Safe Zone'],
      datasets: [
        {
          data: [riskScore, 100 - riskScore],
          backgroundColor: [riskColor, '#e5e7eb'],
          borderColor: ['#1e3a8a', '#d1d5db'],
          borderWidth: 2,
        },
      ],
    }
    
    return (
      <div className="chart-container">
        <h3>FTO Risk Assessment</h3>
        <Pie data={chartData} options={{ maintainAspectRatio: true }} />
        <p className="chart-label risk">{riskScore.toFixed(1)} - {riskLevel}</p>
      </div>
    )
  }

  // Opportunity Score Chart
  const renderOpportunityChart = () => {
    if (!data.unmet_needs) return null
    
    const oppScore = data.unmet_needs.opportunity_score || 0
    
    const chartData = {
      labels: ['Opportunity', 'Remaining'],
      datasets: [
        {
          data: [oppScore, 100 - oppScore],
          backgroundColor: ['#8b5cf6', '#e9d5ff'],
          borderColor: ['#6d28d9', '#ddd6fe'],
          borderWidth: 2,
        },
      ],
    }
    
    return (
      <div className="chart-container">
        <h3>Unmet Needs Opportunity</h3>
        <Pie data={chartData} options={{ maintainAspectRatio: true }} />
        <p className="chart-label">{oppScore.toFixed(1)}/100</p>
      </div>
    )
  }

  return (
    <div className="charts-grid">
      {renderInnovationChart()}
      {renderMarketChart()}
      {renderFTOChart()}
      {renderOpportunityChart()}
    </div>
  )
}
