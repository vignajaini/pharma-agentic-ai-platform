import '../styles/panels.css'

function TradePanel({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <div className="panel-empty">No trade data available</div>
  }

  return (
    <div className="panel">
      <h3>🌍 Trade Data (EXIM)</h3>
      
      <div className="grid-2">
        {data.imports !== undefined && (
          <div className="data-card">
            <h4>Imports</h4>
            <p className="metric-value">
              {typeof data.imports === 'number' ? `${data.imports.toFixed(2)}M` : data.imports}
            </p>
          </div>
        )}
        
        {data.exports !== undefined && (
          <div className="data-card">
            <h4>Exports</h4>
            <p className="metric-value">
              {typeof data.exports === 'number' ? `${data.exports.toFixed(2)}M` : data.exports}
            </p>
          </div>
        )}
      </div>

      {data.countries && (
        <div className="data-card full-width">
          <h4>🌐 Trading Partners</h4>
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Import Volume</th>
                  <th>Export Volume</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(data.countries) && data.countries.map((country, i) => (
                  <tr key={i}>
                    <td>{country.name || country}</td>
                    <td>{country.imports || 'N/A'}</td>
                    <td>{country.exports || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {data.trends && (
        <div className="data-card full-width">
          <h4>📈 Trade Trends</h4>
          <p>{data.trends}</p>
        </div>
      )}

      {data.supply_chain && (
        <div className="data-card full-width">
          <h4>🔗 Supply Chain</h4>
          <p>{data.supply_chain}</p>
        </div>
      )}
    </div>
  )
}

export default TradePanel
