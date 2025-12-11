# Pharma Agentic AI Platform - Frontend

A modern React/Vite frontend for the Pharma Agentic AI Platform with integrated visualization of Molecule Innovation Twin (MIT) data across multiple pharmaceutical research agents.

## Features

✨ **Multi-Agent Dashboard**
- Real-time query interface for molecule analysis
- Results display across 7 specialized agents

📊 **Agent-Specific Panels**
- **Market Panel (IQVIA)** - Market size, CAGR, regional breakdown
- **Trade Panel (EXIM)** - Import/export data, trading partners
- **Patent Panel** - Patent search, filing dates, assignees
- **Clinical Panel** - Trial phases, status, enrollment
- **Web Panel** - External research articles and sources
- **Insights Panel** - Internal company knowledge
- **MIT Panel** - Molecule Innovation Twin with innovation scores

🎨 **Modern UI/UX**
- Responsive design (desktop & mobile)
- Gradient backgrounds and smooth animations
- Interactive tabs and cards
- Loading states and error handling

📄 **Report Generation**
- Download MIT analysis as PDF report
- Comprehensive data export

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── QueryPanel.jsx (Query input form)
│   │   ├── ResultsDisplay.jsx (Results wrapper)
│   │   ├── LoadingSpinner.jsx (Loading animation)
│   │   ├── styles/
│   │   │   └── panels.css (Shared panel styles)
│   │   └── panels/
│   │       ├── MITPanel.jsx
│   │       ├── MarketPanel.jsx
│   │       ├── TradePanel.jsx
│   │       ├── PatentPanel.jsx
│   │       ├── ClinicalPanel.jsx
│   │       ├── WebPanel.jsx
│   │       └── InsightsPanel.jsx
│   ├── App.jsx (Main app component)
│   ├── App.css (App styling)
│   ├── index.css (Global styles)
│   ├── main.jsx (Entry point)
│   └── assets/
├── package.json
├── vite.config.js
└── eslint.config.js
```

## Installation

1. **Install dependencies**
```bash
cd frontend
npm install
```

## Development

1. **Start development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

2. **Ensure backend is running**
Make sure the Flask backend is running on `http://localhost:8000`

```bash
cd backend
python app.py
```

## Building for Production

```bash
npm run build
npm run preview
```

## Component Architecture

### App.jsx
Main application component that manages:
- Query submission to backend API
- Results state management
- Error handling and display
- PDF report download functionality

### QueryPanel.jsx
Sidebar form component with:
- Molecule name input
- Query prompt textarea
- Form validation
- Agent information display
- Example queries

### ResultsDisplay.jsx
Tabbed interface displaying:
- MIT overview and innovation score
- Agent-specific data panels
- Tab navigation
- Results header with timestamp

### Panel Components
Each agent has a dedicated panel component:
- Data formatting and visualization
- Empty state handling
- Responsive grid layouts
- Interactive elements (links, expandable items)

## API Integration

The frontend communicates with the backend via REST API:

### POST /query
```json
{
  "prompt": "What are the market opportunities?",
  "molecule": "Aspirin"
}
```

Response includes data from all agents:
```json
{
  "molecule": "Aspirin",
  "market": {...},
  "trade": {...},
  "patents": [...],
  "trials": [...],
  "web": [...],
  "internal": {...},
  "mit": {...},
  "report": "PDF data"
}
```

### GET /report/:molecule
Downloads PDF report for analyzed molecule

## Styling

The application uses:
- **CSS Variables** for consistent theming
- **CSS Grid & Flexbox** for responsive layouts
- **CSS Animations** for smooth transitions
- **Mobile-first approach** with responsive breakpoints

### Color Scheme
- Primary: #0066cc (Blue)
- Secondary: #f57c00 (Orange)
- Success: #4caf50 (Green)
- Error: #f44336 (Red)

## Performance Optimizations

- React lazy loading (when needed)
- Efficient state management
- Memoized components
- CSS animations (GPU-accelerated)
- Responsive image handling

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Accessibility

- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Screen reader friendly

## Future Enhancements

- [ ] Data export to CSV/Excel
- [ ] Advanced filtering and search
- [ ] Comparison between molecules
- [ ] Historical data trends
- [ ] User authentication
- [ ] Bookmarking/favorites
- [ ] Custom report templates
- [ ] Real-time collaboration features

## Troubleshooting

### Frontend not connecting to backend
- Ensure backend is running on port 8000
- Check CORS settings in Flask app
- Verify API endpoint URLs in App.jsx

### Styling issues
- Clear browser cache (Ctrl+Shift+Delete)
- Check CSS variable definitions in :root
- Verify all CSS imports are correct

### Components not rendering
- Check browser console for errors
- Verify React version compatibility
- Check component imports and exports

## Development Scripts

- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Contributing

1. Follow React best practices
2. Use functional components with hooks
3. Maintain consistent styling
4. Add comments for complex logic
5. Test responsive design

## License

Part of the Pharma Agentic AI Platform project
