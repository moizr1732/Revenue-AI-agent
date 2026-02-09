"""Slack Integration Module - Send alerts and notifications"""
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Any, List


def send_risk_alert(high_risk_deals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Send Slack alert for high-risk deals."""
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    
    if not slack_token or not slack_channel:
        return {"sent": False, "error": "SLACK_BOT_TOKEN or SLACK_CHANNEL not configured"}
    
    try:
        client = WebClient(token=slack_token)
        
        if not high_risk_deals:
            message = "✅ All deals analyzed. No high-risk deals detected."
        else:
            message = f"⚠️ *{len(high_risk_deals)} High-Risk Deal(s) Detected*\n\n"
            for deal in high_risk_deals:
                message += f"• *{deal.get('deal_name')}* - Risk Score: {deal.get('risk_score')}\n"
                message += f"  Reason: {deal.get('risk_reason')}\n\n"
        
        response = client.chat_postMessage(
            channel=slack_channel,
            text=message
        )
        
        return {"sent": True, "timestamp": response.get("ts")}
    except SlackApiError as e:
        return {"sent": False, "error": f"Slack API error: {e.response['error']}"}
    except Exception as e:
        return {"sent": False, "error": str(e)}


def send_analysis_summary(total_deals: int, high_risk_count: int, avg_risk_score: float) -> Dict[str, Any]:
    """Send Slack summary after analysis completes."""
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    
    if not slack_token or not slack_channel:
        return {"sent": False, "error": "Slack credentials not configured"}
    
    try:
        client = WebClient(token=slack_token)
        
        message = f"""
📊 *Analysis Complete*
• Total Deals: {total_deals}
• High-Risk Deals: {high_risk_count}
• Average Risk Score: {avg_risk_score:.1f}
        """
        
        response = client.chat_postMessage(
            channel=slack_channel,
            text=message
        )
        
        return {"sent": True, "timestamp": response.get("ts")}
    except SlackApiError as e:
        return {"sent": False, "error": f"Slack API error: {e.response['error']}"}
    except Exception as e:
        return {"sent": False, "error": str(e)}
