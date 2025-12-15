import { useState } from 'react'
import './QueryPanel.css'

function QueryPanel({ onQuery, disabled }) {
  const [molecule, setMolecule] = useState('')
  const [prompt, setPrompt] = useState('')
  const [validationError, setValidationError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setValidationError('')

    if (!molecule.trim()) {
      setValidationError('Please enter a molecule name')
      return
    }

    if (!prompt.trim()) {
      setValidationError('Please enter a query prompt')
      return
    }

    onQuery(prompt, molecule)
  }

  return (
    <div className="query-panel">
      <h2>🔍 Query MIT System</h2>
      
      <form onSubmit={handleSubmit} className="query-form">
        <div className="form-group">
          <label htmlFor="molecule">Molecule Name *</label>
          <input
            id="molecule"
            type="text"
            placeholder="e.g., Aspirin, Ibuprofen, Metformin..."
            value={molecule}
            onChange={(e) => setMolecule(e.target.value)}
            disabled={disabled}
            className="form-input"
          />
          <p className="form-hint">Enter the drug molecule name to analyze</p>
        </div>

        <div className="form-group">
          <label htmlFor="prompt">Query Prompt *</label>
          <textarea
            id="prompt"
            placeholder="e.g., What are the market opportunities for this molecule? What are the latest clinical trials? What patents exist?"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={disabled}
            className="form-input form-textarea"
            rows="4"
          />
          <p className="form-hint">Ask specific questions about the molecule</p>
        </div>

        {validationError && (
          <div className="validation-error">
            {validationError}
          </div>
        )}

        <button 
          type="submit" 
          disabled={disabled}
          className="submit-btn"
        >
          {disabled ? '⏳ Analyzing...' : '🚀 Analyze Molecule'}
        </button>
      </form>

      <div className="query-examples">
        <h3>Quick Examples</h3>
        <div className="example-item">
          <p><strong>Market Analysis:</strong> "What is the market size and growth potential?"</p>
        </div>
        <div className="example-item">
          <p><strong>Clinical Status:</strong> "What are the current clinical trials?"</p>
        </div>
        <div className="example-item">
          <p><strong>Patent Landscape:</strong> "What patents exist for this molecule?"</p>
        </div>
        <div className="example-item">
          <p><strong>Trade Flow:</strong> "What are the import/export patterns?"</p>
        </div>
      </div>

      <div className="agent-info">
        <h3>Active Agents</h3>
        <ul>
          <li>📊 IQVIA Agent - Market data</li>
          <li>🌍 EXIM Agent - Trade flows</li>
          <li>📜 Patent Agent - IP research</li>
          <li>🧪 Clinical Agent - Trial data</li>
          <li>🌐 Web Agent - External sources</li>
          <li>📚 Internal Agent - Company docs</li>
          <li>📄 Report Agent - PDF generation</li>
        </ul>
      </div>
    </div>
  )
}

export default QueryPanel
