import { useState } from 'react'
import './App.css'
import QueryPanel from './components/QueryPanel'
import ResultsDisplay from './components/ResultsDisplay'
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleQuery = async (prompt, molecule) => {
    setLoading(true)
    setError(null)
    setResults(null)

    // Real-time streaming via Server-Sent Events (SSE)
    try {
      const url = `http://localhost:8000/stream-query?molecule=${encodeURIComponent(molecule)}&prompt=${encodeURIComponent(prompt)}`
      const es = new EventSource(url)

      es.onmessage = (evt) => {
        try {
          const payload = JSON.parse(evt.data)
          // Handle types: status, agent, mit, unmet_needs, fto, report, done, error, llm_token
          if (payload.type === 'done') {
            setResults(payload.result)
            setLoading(false)
            es.close()
            return
          }

          if (payload.type === 'error') {
            setError(payload.message || 'Stream error')
            setLoading(false)
            es.close()
            return
          }

          if (payload.type === 'agent') {
            // Store per-agent data under results.agents.<agentName>
            setResults(prev => ({
              ...(prev || {}),
              agents: {
                ...((prev && prev.agents) || {}),
                [payload.agent]: payload.data
              }
            }))
            return
          }

          if (payload.type === 'llm_token') {
            // Append token to a streaming buffer under results.llm_stream
            setResults(prev => ({
              ...(prev || {}),
              llm_stream: ((prev && prev.llm_stream) || '') + (payload.data || '')
            }))
            return
          }

          // Default: store by type key (mit, unmet_needs, fto, report, status, etc.)
          setResults(prev => ({ ...(prev || {}), [payload.type]: payload.data || payload }))

        } catch (e) {
          console.error('Failed to parse stream event', e)
        }
      }

      es.onerror = (err) => {
        console.error('EventSource error', err)
        setError('Streaming connection error')
        setLoading(false)
        es.close()
      }

    } catch (err) {
      setError(err.message || 'Failed to start streaming')
      setLoading(false)
    }
  }

  const handleDownloadReport = async (molecule) => {
    try {
      const response = await fetch(`http://localhost:8000/report/${molecule}`)
      if (!response.ok) {
        throw new Error('Failed to download report')
      }
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${molecule}_report.pdf`
      a.click()
    } catch (err) {
      setError('Failed to download report: ' + err.message)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>💊 InnoMed.AI</h1>
        <p className="subtitle">Molecule Innovation Twin (MIT) Discovery System</p>
      </header>

      <main className="app-main">
        <div className="sidebar">
          <QueryPanel onQuery={handleQuery} disabled={loading} />
        </div>

        <div className="content">
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              {error}
              <button onClick={() => setError(null)} className="close-btn">✕</button>
            </div>
          )}

          {loading && <LoadingSpinner />}

          {results && !loading && (
            <ResultsDisplay 
              results={results} 
              onDownloadReport={() => handleDownloadReport(results.molecule)}
            />
          )}

          {!loading && !results && !error && (
            <div className="empty-state">
              <div className="empty-icon">🔬</div>
              <h2>Welcome to MIT Discovery</h2>
              <p>Enter a molecule name and query to analyze pharmaceutical data across multiple agents</p>
              <div className="info-grid">
                <div className="info-card">
                  <span className="info-icon">📊</span>
                  <h3>Market Data</h3>
                  <p>IQVIA market analysis</p>
                </div>
                <div className="info-card">
                  <span className="info-icon">🌍</span>
                  <h3>Trade Data</h3>
                  <p>EXIM trade flows</p>
                </div>
                <div className="info-card">
                  <span className="info-icon">📜</span>
                  <h3>Patents</h3>
                  <p>Patent intelligence</p>
                </div>
                <div className="info-card">
                  <span className="info-icon">🧪</span>
                  <h3>Clinical Trials</h3>
                  <p>Research status</p>
                </div>
                <div className="info-card">
                  <span className="info-icon">🌐</span>
                  <h3>Web Research</h3>
                  <p>External sources</p>
                </div>
                <div className="info-card">
                  <span className="info-icon">📚</span>
                  <h3>Internal Insights</h3>
                  <p>Company knowledge</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
