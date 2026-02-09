"""Agent Service Module - Core Business Logic"""
from datetime import datetime
from typing import List, Dict, Any
from crm_integration import fetch_hubspot_deals
from ai_scoring import calculate_risk_score
from sheets_integration import sync_deals_to_sheets
from slack_integration import send_risk_alert, send_analysis_summary


# Global state
analyzed_deals: List[Dict[str, Any]] = []
last_analysis: str = None


async def run_complete_analysis(sheet_id: str = None, send_slack: bool = True) -> Dict[str, Any]:
    """
    Run complete analysis workflow:
    1. Fetch HubSpot deals
    2. Calculate AI risk scores
    3. Sync to Google Sheets
    4. Send Slack alert
    
    Args:
        sheet_id: Google Sheet ID to sync to (optional)
        send_slack: Whether to send Slack notifications (optional)
    """
    global analyzed_deals, last_analysis
    
    try:
        # Fetch deals from HubSpot
        deals = await fetch_hubspot_deals(limit=100)
        
        analyzed_deals = []
        for deal in deals:
            deal_id = deal.get("id")
            props = deal.get("properties", {})
            
            # Calculate risk score with AI
            risk_analysis = await calculate_risk_score(deal)
            
            # Build deal object
            deal_obj = {
                "deal_id": deal_id,
                "deal_name": props.get("dealname", "Unknown"),
                "stage": props.get("dealstage", "Unknown"),
                "risk_score": risk_analysis["risk_score"],
                "risk_reason": risk_analysis["risk_reason"],
                "timestamp": datetime.now().isoformat(),
                "amount": props.get("amount", 0)
            }
            analyzed_deals.append(deal_obj)
        
        last_analysis = datetime.now().isoformat()
        
        # Sync to Google Sheets if sheet_id provided
        if sheet_id:
            try:
                await sync_deals_to_sheets(sheet_id, analyzed_deals)
            except Exception as e:
                print(f"Google Sheets sync error: {e}")
        
        # Send Slack alerts if enabled
        if send_slack:
            high_risk_deals = [d for d in analyzed_deals if d.get("risk_score", 0) >= 70]
            if high_risk_deals:
                send_risk_alert(high_risk_deals)
            
            avg_score = sum(d.get("risk_score", 0) for d in analyzed_deals) / len(analyzed_deals) if analyzed_deals else 0
            send_analysis_summary(len(analyzed_deals), len(high_risk_deals), avg_score)
        
        return {
            "status": "success",
            "message": f"Analyzed {len(analyzed_deals)} deals",
            "timestamp": last_analysis,
            "deals_count": len(analyzed_deals)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }


def get_analyzed_deals() -> List[Dict[str, Any]]:
    """Get all analyzed deals from last analysis."""
    return analyzed_deals.copy()


def get_last_analysis_time() -> str:
    """Get timestamp of last analysis."""
    return last_analysis


def get_risk_summary() -> Dict[str, Any]:
    """Get summary statistics of analyzed deals."""
    if not analyzed_deals:
        return {
            "total_deals": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "avg_risk_score": 0
        }
    
    high_risk = [d for d in analyzed_deals if d.get("risk_score", 0) >= 70]
    medium_risk = [d for d in analyzed_deals if 40 <= d.get("risk_score", 0) < 70]
    low_risk = [d for d in analyzed_deals if d.get("risk_score", 0) < 40]
    
    avg_score = sum(d.get("risk_score", 0) for d in analyzed_deals) / len(analyzed_deals)
    
    return {
        "total_deals": len(analyzed_deals),
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(medium_risk),
        "low_risk_count": len(low_risk),
        "avg_risk_score": round(avg_score, 1),
        "last_analysis": last_analysis
    }
