# Pharma Agentic AI Platform - Backend

A comprehensive multi-agent system for pharmaceutical research and analysis using Flask and specialized worker agents.

## Features

✨ **7 Specialized Agents:**
- 📊 **IQVIA Agent** - Market intelligence and size analysis
- 🌍 **EXIM Agent** - Trade flow and import/export data
- 📜 **Patent Agent** - Patent landscape analysis
- 🧪 **Clinical Agent** - Clinical trials research
- 🌐 **Web Agent** - External research and literature
- 📚 **Internal Insights Agent** - Company knowledge base analysis
- 📄 **Report Generator** - PDF report generation

💡 **Core Capabilities:**
- Molecule Innovation Twin (MIT) creation
- Innovation scoring algorithm
- Intelligent request caching
- Comprehensive error handling
- Request validation
- Structured logging
- RESTful API with v1.0 versioning

## Architecture

```
backend/
├── app.py                      # Main Flask application
├── master_agent.py             # Master orchestration agent
├── config.py                   # Configuration management
├── utils.py                    # Utilities (cache, validation, formatting)
├── iqvia_agent.py             # Market agent
├── exim_agent.py              # Trade agent
├── patent_agent.py            # Patent agent
├── clinical_agent.py          # Clinical trials agent
├── web_agent.py               # Web research agent
├── internal_insights_agent.py # Internal knowledge agent
├── report_generator_agent.py  # PDF report generation
├── mit/
│   ├── __init__.py
│   ├── mit_builder.py         # MIT profile builder
│   └── innovation_score.py    # Innovation scoring
├── data/                       # Mock data files
│   ├── mock_iqvia.json
│   ├── mock_exim.json
│   ├── mock_patents.json
│   └── mock_trials.json
├── API_DOCUMENTATION.md       # Full API documentation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize:

```python
API_CONFIG = {
    'MAX_MOLECULE_LENGTH': 100,
    'MAX_PROMPT_LENGTH': 2000,
    'CACHE_ENABLED': True,
    'CACHE_TTL': 3600,  # 1 hour
    'LOG_REQUESTS': True,
}
```

## Running the Backend

```bash
python app.py
```

The server will start on `http://127.0.0.1:8000`

### Debug Mode
The application runs in Flask debug mode by default. For production:

Edit `app.py` last line:
```python
app.run(debug=False, port=8000)
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8000/
GET http://localhost:8000/health
```

### Analyze Molecule
```bash
POST http://localhost:8000/api/v1/query
Content-Type: application/json

{
  "molecule": "Aspirin",
  "prompt": "What is the market potential?"
}
```

### Retrieve MIT
```bash
GET http://localhost:8000/api/v1/mit/Aspirin
```

### Download Report
```bash
GET http://localhost:8000/api/v1/report/Aspirin
```

### Cache Management
```bash
GET http://localhost:8000/api/v1/cache/stats
POST http://localhost:8000/api/v1/cache/clear
```

### List Agents
```bash
GET http://localhost:8000/api/v1/agents
```

## Full API Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete endpoint reference, request/response formats, and examples.

## Data Models

### Molecule Innovation Twin (MIT)
```json
{
  "molecule": "Aspirin",
  "innovation_score": 75.5,
  "market": { /* market data */ },
  "trade": { /* trade data */ },
  "patents": [ /* patent documents */ ],
  "trials": [ /* clinical trials */ ],
  "web": { /* web research */ },
  "internal": { /* internal insights */ },
  "highlights": [ /* key findings */ ],
  "metadata": {
    "created_at": "2024-12-15T10:30:00",
    "agents_used": 7
  }
}
```

## Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `pharma_backend.log`

Log levels: DEBUG, INFO, WARNING, ERROR

## Caching System

- **Automatic caching** of analysis results
- **TTL-based expiration**: 1 hour default
- **Cache key** generated from molecule + prompt hash
- **Management endpoints** to view and clear cache

## Error Handling

The API provides consistent error responses:

```json
{
  "status": "error",
  "code": 400,
  "message": "Validation failed",
  "timestamp": "2024-12-15T10:30:00",
  "errors": ["error1", "error2"]
}
```

Error codes:
- `400` - Validation errors
- `404` - Resource not found
- `500` - Server errors

## Agent System

Each agent is independent and can fail gracefully:

```python
market = self._safe_call(self.iqvia.fetch_market, molecule)
# Returns None if agent fails, but doesn't crash the system
```

## Performance

- **Average response time**: 2-3 seconds
- **Cache hit**: <100ms
- **Concurrency**: Supports multiple simultaneous requests

## Development

### Adding a New Agent

1. Create `new_agent.py`
2. Implement class with main method
3. Add to `MasterAgent.__init__`
4. Update MIT builder to include new data

Example:
```python
class NewAgent:
    def analyze(self, molecule):
        return {"result": "data"}
```

### Extending Configuration

Edit `config.py` and add new settings:
```python
API_CONFIG['NEW_SETTING'] = value
```

## Testing

Run with sample molecule:
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"molecule": "Aspirin", "prompt": "Analyze this molecule"}'
```

## Troubleshooting

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, port=8001)
```

### Module Not Found
Ensure you're in the backend directory and virtual environment is activated.

### CORS Errors
CORS is already enabled globally via Flask-CORS.

### Cache Issues
Clear cache via API:
```bash
POST http://localhost:8000/api/v1/cache/clear
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| Flask-CORS | 4.0.0 | CORS support |
| reportlab | 4.4.5 | PDF generation |
| python-dotenv | 1.0.0 | Environment variables |

## Contributing

To improve the backend:
1. Follow the existing code structure
2. Add logging for debugging
3. Include error handling
4. Update documentation

## License

This project is part of the Pharma Agentic AI Platform.

## Support

For issues or questions:
- Check API_DOCUMENTATION.md
- Review pharma_backend.log for errors
- Check configuration in config.py

## Version

**Current Version**: 1.0.0 (December 15, 2024)

**Last Updated**: December 15, 2024
