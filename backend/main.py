from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

from agent_service import (
    run_complete_analysis,
    get_analyzed_deals,
    get_last_analysis_time,
    get_risk_summary
)
from crm_integration import test_hubspot_connection, fetch_hubspot_deals
from sheets_integration import sync_deals_to_sheets, read_sheets

# Load environment variables
load_dotenv()

app = FastAPI(title="Revenue AI Agent API")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://revenue-ai-agent.vercel.app"  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample fallback data
sample_deals = [
    {
        "deal_id": "demo_001",
        "deal_name": "Acme Corp Contract",
        "stage": "Proposal",
        "risk_score": 35,
        "risk_reason": "Large contract value with tight timeline",
        "timestamp": datetime.now().isoformat()
    },
    {
        "deal_id": "demo_002",
        "deal_name": "Tech Solutions Inc",
        "stage": "Negotiation",
        "risk_score": 55,
        "risk_reason": "Multiple stakeholders with competing priorities",
        "timestamp": datetime.now().isoformat()
    },
    {
        "deal_id": "demo_003",
        "deal_name": "Global Industries Ltd",
        "stage": "Closing",
        "risk_score": 75,
        "risk_reason": "Established client with clear requirements",
        "timestamp": datetime.now().isoformat()
    }
]


# ============================================================================
# REST API Routes
# ============================================================================

@app.get("/")
async def read_root():
    """Health check endpoint"""
    return {"message": "Revenue AI Agent API", "status": "running"}


@app.get("/api/hubspot/test")
async def hubspot_test():
    """Test HubSpot connectivity"""
    return await test_hubspot_connection()


@app.get("/api/hubspot/deals")
async def api_hubspot_deals(limit: int = 100):
    """Get raw deals from HubSpot"""
    try:
        deals = await fetch_hubspot_deals(limit=limit)
        return {"count": len(deals), "deals": deals}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/analyze")
async def trigger_analysis(sheet_id: str = None):
    """
    Run complete analysis workflow:
    - Fetch HubSpot deals
    - Calculate AI risk scores
    - Sync to Google Sheets (optional)
    - Send Slack alerts (optional)
    """
    sheet_id = sheet_id or "1IradqvjgkrRNkdYa13qUsLgPzNq0YCCUjDV3mwGgvZg"
    return await run_complete_analysis(sheet_id=sheet_id, send_slack=True)


@app.get("/api/deals")
async def get_deals():
    """Get analyzed deals from last analysis"""
    deals = get_analyzed_deals()
    if deals:
        return {"deals": deals, "count": len(deals)}
    else:
        return {"deals": sample_deals, "count": len(sample_deals)}


@app.get("/api/status")
async def get_status():
    """Get API status and analysis information"""
    summary = get_risk_summary()
    return {
        "status": "running",
        "last_analysis": get_last_analysis_time(),
        "summary": summary
    }


@app.post("/api/hubspot/sync")
async def hubspot_sync(sheet_id: str = None):
    """Manually sync analyzed deals to Google Sheets"""
    sheet_id = sheet_id or "1IradqvjgkrRNkdYa13qUsLgPzNq0YCCUjDV3mwGgvZg"
    deals = get_analyzed_deals()
    
    if not deals:
        return {"synced": False, "error": "No analyzed deals to sync"}
    
    return await sync_deals_to_sheets(sheet_id, deals)


@app.get("/api/sheets/read")
async def sheets_read(sheet_id: str = None):
    """Read data from Google Sheet"""
    sheet_id = sheet_id or "1IradqvjgkrRNkdYa13qUsLgPzNq0YCCUjDV3mwGgvZg"
    return await read_sheets(sheet_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
