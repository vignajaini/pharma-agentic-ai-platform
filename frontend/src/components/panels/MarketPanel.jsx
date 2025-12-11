import '../styles/panels.css'

function MarketPanel({ data }) {
  if (!data) {
    return <div className="panel-empty">No market data available</div>
  }

  return (
    <div className="panel">
      <h3>📊 Market Data (IQVIA)</h3>
      
      <div className="grid-2">
        {data.market_size !== undefined && (
          <div className="data-card">
            <h4>Market Size</h4>
            <p className="metric-value">
              {typeof data.market_size === 'number' 
                ? `$${(data.market_size / 1000000).toFixed(2)}M`
                : data.market_size
              }
            </p>
          </div>
        )}
        
        {data.cagr !== undefined && (
          <div className="data-card">
            <h4>CAGR (Growth Rate)</h4>
            <p className="metric-value">
              {typeof data.cagr === 'number' ? `${data.cagr.toFixed(2)}%` : data.cagr}
            </p>
          </div>
        )}
      </div>

      {data.regions && (
        <div className="data-card full-width">
          <h4>📍 Regional Breakdown</h4>
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Region</th>
                  <th>Market Size</th>
                  <th>Growth Rate</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(data.regions) && data.regions.map((region, i) => (
                  <tr key={i}>
                    <td>{region.name || region}</td>
                    <td>{region.size || 'N/A'}</td>
                    <td>{region.growth || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {data.competitive_landscape && (
        <div className="data-card full-width">
          <h4>🏆 Competitive Landscape</h4>
          <p>{data.competitive_landscape}</p>
        </div>
      )}

      {data.key_players && (
        <div className="data-card full-width">
          <h4>Companies</h4>
          <ul className="data-list">
            {Array.isArray(data.key_players) && data.key_players.map((player, i) => (
              <li key={i}>{player}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default MarketPanel
