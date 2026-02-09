"""AI Scoring Module - OpenAI Integration for Risk Analysis"""
import os
import json
from typing import Dict, Any


async def calculate_risk_score(deal_info: dict) -> Dict[str, Any]:
    """Use OpenAI to calculate risk score for a deal."""
    from openai import OpenAI
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        # Return default if no OpenAI key
        return {
            "risk_score": 50,
            "risk_reason": "OpenAI key not configured"
        }
    
    client = OpenAI(api_key=openai_key)
    
    deal_name = deal_info.get("properties", {}).get("dealname", "Unknown Deal")
    amount = deal_info.get("properties", {}).get("amount", "Unknown")
    stage = deal_info.get("properties", {}).get("dealstage", "Unknown")
    
    prompt = f"""Analyze this sales deal and provide a risk score (0-100, where 100 is safest):
Deal: {deal_name}
Amount: {amount}
Stage: {stage}

Respond with JUST a JSON object (no markdown, no code blocks): {{"risk_score": <0-100>, "risk_reason": "<brief reason>"}}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        # Parse JSON response
        result = json.loads(response_text)
        return {
            "risk_score": min(100, max(0, int(result.get("risk_score", 50)))),
            "risk_reason": result.get("risk_reason", "AI Analysis")
        }
    except Exception as e:
        return {
            "risk_score": 50,
            "risk_reason": f"Analysis error: {str(e)[:50]}"
        }
