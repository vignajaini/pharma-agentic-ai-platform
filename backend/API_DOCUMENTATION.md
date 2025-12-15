# Pharma Agentic AI Platform - Backend API Documentation

## Overview
This is a comprehensive backend API for pharmaceutical research analysis using multiple specialized agents.

**Base URL:** `http://localhost:8000`
**API Version:** 1.0.0

---

## Endpoints

### 1. Health & Status

#### GET `/`
Health check and API information

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Backend is operational",
  "data": {
    "service": "Pharma Agentic AI Platform Backend",
    "version": "1.0.0",
    "status": "operational",
    "timestamp": "2024-12-15T10:30:00"
  }
}
```

#### GET `/health`
Simple health status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-15T10:30:00"
}
```

---

### 2. Molecule Analysis

#### POST `/api/v1/query`
Analyze a molecule across all agents (IQVIA, EXIM, Patents, Clinical, Web, Internal, Reports)

**Request:**
```json
{
  "molecule": "Aspirin",
  "prompt": "What is the market potential and current research status for this molecule?"
}
```

**Parameters:**
- `molecule` (string, required): Name of the molecule (1-100 characters)
- `prompt` (string, required): Research query or question (1-2000 characters)

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Analysis complete",
  "data": {
    "molecule": "Aspirin",
    "market": { /* IQVIA data */ },
    "trade": { /* EXIM data */ },
    "patents": [ /* Patent documents */ ],
    "trials": [ /* Clinical trials */ ],
    "web": { /* Web research */ },
    "internal": { /* Internal insights */ },
    "mit": {
      "molecule": "Aspirin",
      "innovation_score": 75.5,
      "highlights": [ /* Key findings */ ],
      "metadata": { "created_at": "2024-12-15T10:30:00" }
    },
    "report": "/path/to/report.pdf",
    "processing_time_seconds": 2.34,
    "timestamp": "2024-12-15T10:30:00"
  }
}
```

**Error Response (400 - Validation):**
```json
{
  "status": "error",
  "code": 400,
  "message": "Validation failed",
  "timestamp": "2024-12-15T10:30:00",
  "errors": [
    "Molecule name is required",
    "Prompt is required"
  ]
}
```

**Error Response (500 - Server):**
```json
{
  "status": "error",
  "code": 500,
  "message": "Failed to process query: Database connection error",
  "timestamp": "2024-12-15T10:30:00"
}
```

---

### 3. MIT Retrieval

#### GET `/api/v1/mit/<molecule>`
Retrieve previously analyzed MIT for a molecule

**Parameters:**
- `molecule` (path, required): Molecule name

**Example:** `GET /api/v1/mit/Aspirin`

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "MIT retrieved for Aspirin",
  "data": {
    "molecule": "Aspirin",
    "innovation_score": 75.5,
    "market": { /* ... */ },
    "trade": { /* ... */ },
    "patents": [ /* ... */ ],
    "trials": [ /* ... */ ],
    "web": { /* ... */ },
    "internal": { /* ... */ },
    "highlights": [
      "Market size: $2,500,000,000",
      "CAGR: 5.5%",
      "3 active patents",
      "5 clinical trials found"
    ]
  }
}
```

**Error Response (404):**
```json
{
  "status": "error",
  "code": 404,
  "message": "No MIT found for molecule: Unknown",
  "timestamp": "2024-12-15T10:30:00"
}
```

---

### 4. Report Download

#### GET `/api/v1/report/<molecule>`
Download PDF report for a molecule

**Parameters:**
- `molecule` (path, required): Molecule name

**Example:** `GET /api/v1/report/Aspirin`

**Response:**
- File download (application/pdf)
- Filename: `{molecule}_report.pdf`

**Error Response (404):**
```json
{
  "status": "error",
  "code": 404,
  "message": "No MIT found for molecule: Unknown",
  "timestamp": "2024-12-15T10:30:00"
}
```

---

### 5. Cache Management

#### GET `/api/v1/cache/stats`
Get cache statistics

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Cache statistics",
  "data": {
    "cached_items": 5,
    "ttl_seconds": 3600
  }
}
```

#### POST `/api/v1/cache/clear`
Clear all cached analysis results

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Cache cleared successfully",
  "data": {
    "cleared": true
  }
}
```

---

### 6. Agent Information

#### GET `/api/v1/agents`
List all available analysis agents

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Available agents",
  "data": {
    "market": "IQVIA Agent - Market data and size",
    "trade": "EXIM Agent - Import/export flows",
    "patents": "Patent Agent - Patent information",
    "trials": "Clinical Trials Agent - Research status",
    "web": "Web Agent - External research",
    "internal": "Internal Insights Agent - Company knowledge",
    "report": "Report Generator - PDF generation"
  }
}
```

---

## Data Models

### Molecule Innovation Twin (MIT)
```json
{
  "molecule": "string",
  "innovation_score": "number (0-100)",
  "market": "object",
  "trade": "object",
  "patents": "array",
  "trials": "array",
  "web": "object",
  "internal": "object",
  "highlights": "array of strings",
  "metadata": {
    "created_at": "ISO 8601 timestamp",
    "agents_used": "number"
  }
}
```

### Market Data (IQVIA)
```json
{
  "market_size": "number",
  "cagr": "number (percentage)",
  "regions": [
    {
      "name": "string",
      "size": "number",
      "growth": "number"
    }
  ],
  "key_players": "array of strings",
  "competitive_landscape": "string",
  "forecast": "string"
}
```

### Trade Data (EXIM)
```json
{
  "imports": "number",
  "exports": "number",
  "countries": [
    {
      "name": "string",
      "imports": "number",
      "exports": "number"
    }
  ],
  "trends": "string"
}
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Validation failed or invalid input |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |
| 504 | Timeout | Request timeout |

---

## Request/Response Headers

### Recommended Headers
```
Content-Type: application/json
Accept: application/json
```

### CORS
All endpoints support CORS. Requests from any origin are accepted.

---

## Rate Limiting & Caching

- **Cache TTL:** 3600 seconds (1 hour)
- **Cache Key:** Generated from molecule name + prompt
- **Max Molecule Length:** 100 characters
- **Max Prompt Length:** 2000 characters

---

## Logging

All requests are logged to:
- Console: Real-time output
- File: `pharma_backend.log`

Log levels:
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Errors
- DEBUG: Detailed information

---

## Example Usage

### Using cURL
```bash
# Analyze a molecule
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "molecule": "Aspirin",
    "prompt": "What is the market potential for this molecule?"
  }'

# Get MIT
curl http://localhost:8000/api/v1/mit/Aspirin

# Download report
curl -O http://localhost:8000/api/v1/report/Aspirin

# Check cache stats
curl http://localhost:8000/api/v1/cache/stats
```

### Using Python
```python
import requests

url = "http://localhost:8000/api/v1/query"
data = {
    "molecule": "Aspirin",
    "prompt": "What is the market potential for this molecule?"
}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'success':
    print(f"Analysis complete: {result['data']['mit']['innovation_score']}")
else:
    print(f"Error: {result['message']}")
```

### Using JavaScript/Fetch
```javascript
const data = {
  molecule: "Aspirin",
  prompt: "What is the market potential for this molecule?"
};

fetch('http://localhost:8000/api/v1/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => {
  if (result.status === 'success') {
    console.log('Innovation Score:', result.data.mit.innovation_score);
  }
});
```

---

## Version History

### v1.0.0 (December 15, 2024)
- Initial release
- 7 agent system
- MIT generation and caching
- PDF report generation
- Comprehensive error handling
- Request validation
- Logging system

---

## Support

For issues or questions, please refer to the project repository or contact the development team.
