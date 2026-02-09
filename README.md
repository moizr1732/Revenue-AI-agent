# Revenue AI Agent - Intelligent Sales Deal Analyzer

> Analyze sales deals with AI-powered risk scoring, integrated with HubSpot, Google Sheets, and Slack.

## 📁 Project Structure

```
revenue-ai-agent/
├── backend/
│   ├── main.py                    # FastAPI app & REST API routes
│   ├── agent_service.py           # Core analysis workflow logic
│   ├── crm_integration.py         # HubSpot CRM integration
│   ├── ai_scoring.py              # OpenAI risk scoring
│   ├── sheets_integration.py      # Google Sheets sync
│   ├── slack_integration.py       # Slack notifications
│   ├── requirements.txt           # Python dependencies
│   └── vercel.json               # Vercel deployment config
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── App.jsx                # Main router
│   │   ├── main.jsx               # Entry point
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js             # Vite dev server setup
│   ├── tailwind.config.js         # Tailwind styling
│   └── postcss.config.js
├── .env                           # Environment variables (local)
├── .env.example                   # Example env template
├── .gitignore
└── README.md                      # This file
```

## 🎯 Features

- **HubSpot Integration**: Automatically fetch deals from your HubSpot CRM
- **AI Risk Scoring**: OpenAI-powered analysis to assess deal risk (0-100 scale)
- **Google Sheets Sync**: Persist analyzed deals to Google Sheets
- **Slack Alerts**: Send notifications for high-risk deals
- **Modern Dashboard**: React + Tailwind UI with real-time deal metrics
- **Modular Architecture**: Organized backend with separate modules for each integration

## 🚀 Quick Start

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file with required credentials:**
   ```env
   OPENAI_API_KEY=sk-proj-your-key-here
   HUBSPOT_TOKEN=pat-na2-your-token-here
   SLACK_BOT_TOKEN=xoxb-your-token-here
   SLACK_CHANNEL=C0ADUC4CL9J
   GOOGLE_CREDENTIALS_FILE=/path/to/gsa-key.json
   BACKEND_HOST=localhost
   BACKEND_PORT=8000
   ```

4. **Run the backend:**
   ```bash
   python main.py
   ```
   Backend available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend available at: `http://localhost:3000`

## 📊 Dashboard Features

- **Deal Risk Dashboard**: View analyzed deals with AI-calculated risk scores
- **Real-time Metrics**: Total deals, high-risk count, average risk score
- **Visual Analytics**: Risk distribution chart (High/Medium/Low)
- **Auto Refresh**: Dashboard updates every 30 seconds
- **One-Click Analysis**: Run AI analysis with the "Run Analysis" button
- **Google Sheets Integration**: View and manage deal data in the Sheets tab

## 🔧 Backend Modules

### `main.py`
- FastAPI application server
- CORS middleware for frontend communication
- REST API route definitions
- Entry point: `if __name__ == "__main__"`

### `agent_service.py`
Core business logic for the analysis workflow:
- `run_complete_analysis()` - Main analysis function
- `get_risk_summary()` - Get deal statistics
- `get_analyzed_deals()` - Retrieve analyzed deals

### `crm_integration.py`
HubSpot CRM integration:
- `fetch_hubspot_deals()` - Get deals from HubSpot API
- `test_hubspot_connection()` - Verify API connectivity

### `ai_scoring.py`
OpenAI risk analysis:
- `calculate_risk_score()` - Use GPT to analyze deal risk (0-100 scale)

### `sheets_integration.py`
Google Sheets persistence:
- `sync_deals_to_sheets()` - Write analyzed deals to Google Sheet
- `read_sheets()` - Read data from Google Sheet
- `get_google_client()` - Authenticate with service account

### `slack_integration.py`
Slack notifications:
- `send_risk_alert()` - Alert for high-risk deals
- `send_analysis_summary()` - Send analysis completion summary

## 🔐 Security

⚠️ **Never commit `.env` to version control!**

The `.gitignore` file excludes:
- `.env` files
- `node_modules/`, `venv/`
- Build artifacts
- IDE settings

### Environment Variable Setup

1. **Get OpenAI API Key:**
   - Visit: https://platform.openai.com/api-keys
   - Create new secret key
   - Add to `.env`

2. **Get HubSpot Token:**
   - Log in to HubSpot
   - Settings → Integrations → Private apps
   - Create app and generate token
   - Add to `.env`

3. **Get Slack Credentials:**
   - Go to: https://api.slack.com/apps
   - Create new app
   - Install to workspace
   - Get Bot Token (xoxb-...)
   - Find channel ID (right-click channel → Copy channel ID)
   - Add to `.env`

4. **Get Google Service Account:**
   - Go to Google Cloud Console
   - Create new project
   - Enable Google Sheets API
   - Create Service Account
   - Download JSON key file
   - Share Google Sheet with service account email
   - Add file path to `.env`

## 📡 API Endpoints

### Analysis & Data
- `POST /api/analyze` - Run deal analysis workflow
- `GET /api/deals` - Get analyzed deals
- `GET /api/status` - Get API status and last analysis time
- `GET /api/hubspot/test` - Test HubSpot connectivity
- `GET /api/hubspot/deals` - Get raw HubSpot deals

### Google Sheets
- `POST /api/hubspot/sync` - Sync deals to Google Sheet
- `GET /api/sheets/read` - Read from Google Sheet

## 🎨 Frontend Components

- **App.jsx** - Main router (`/` and `/sheets` routes)
- **Dashboard.jsx** - Main dashboard view
- **Metrics.jsx** - KPI cards (Total, Risky, Avg Score, Last Analysis)
- **DealCard.jsx** - Individual deal display with risk level
- **RiskChart.jsx** - Bar chart showing risk distribution
- **SheetView.jsx** - Google Sheets viewer
- **AnalysisControls.jsx** - Run Analysis button
- **Sidebar.jsx** - Navigation menu
- **Navbar.jsx** - Header with title and status

## 📦 Deployment

### Vercel (Backend)
```bash
vercel deploy
```
Uses `backend/vercel.json` for configuration.

### Production Environment Variables
Set these in your deployment platform:
- `OPENAI_API_KEY`
- `HUBSPOT_TOKEN`
- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL`
- `GOOGLE_CREDENTIALS_FILE`

### Vercel Frontend
```bash
cd frontend
vercel deploy
```

## 🧪 Testing

### Test HubSpot Connection
```bash
curl http://localhost:8000/api/hubspot/test
```

### Trigger Analysis
```bash
curl -X POST http://localhost:8000/api/analyze
```

### Get Analyzed Deals
```bash
curl http://localhost:8000/api/deals
```

## 📚 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- OpenAI (GPT-3.5-turbo for AI analysis)
- httpx (Async HTTP client)
- gspread (Google Sheets API)
- slack-sdk (Slack integration)
- python-dotenv (Environment variables)

**Frontend:**
- React 18 (UI framework)
- Vite (Build tool)
- Tailwind CSS (Styling)
- React Router (Navigation)
- Axios (HTTP client)
- Lucide React (Icons)

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (requires 3.8+)
- Verify all dependencies: `pip list`
- Check `.env` file exists and is readable
- Ensure port 8000 is not in use: `lsof -i :8000`

### Google Sheets sync not working
- Verify service account email is shared on the sheet
- Check `GOOGLE_CREDENTIALS_FILE` path is correct
- Ensure JSON file has valid permissions

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check `vite.config.js` proxy settings
- Ensure CORS is enabled in `main.py`

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [HubSpot API Docs](https://developers.hubspot.com/)
- [Slack API Docs](https://api.slack.com/)
```bash
npm run build
```

This creates optimized files in the `dist/` directory ready for deployment.

## 🐛 Troubleshooting

**Frontend can't connect to backend?**
- Ensure backend is running on `http://localhost:8000`
- Check CORS configuration in `backend/main.py`
- Check Vite proxy settings in `frontend/vite.config.js`

**Dependencies not installing?**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules/` and `package-lock.json`, then reinstall
- For backend: try using `pip install --upgrade pip` first

**Components not styling correctly?**
- Rebuild Tailwind: `npm run build` and `npm run dev`
- Check that Tailwind CSS is imported in `src/index.css`
