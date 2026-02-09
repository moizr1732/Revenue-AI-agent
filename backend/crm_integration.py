"""HubSpot CRM Integration Module"""
import os
import httpx
from typing import List, Dict, Any


async def fetch_hubspot_deals(limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch deals from HubSpot API (returns list of deal objects)."""
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        raise RuntimeError("HUBSPOT_TOKEN not set in environment")

    # Request some common deal properties; adjust as needed
    props = ["dealname", "amount", "dealstage", "closedate", "hs_lastmodifieddate"]
    url = f"https://api.hubapi.com/crm/v3/objects/deals?limit={limit}&properties={','.join(props)}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=headers)

    if r.status_code != 200:
        raise RuntimeError(f"HubSpot API error: {r.status_code} - {r.text}")

    data = r.json()
    return data.get("results", [])


async def test_hubspot_connection() -> Dict[str, Any]:
    """Quick check to verify HubSpot connectivity using HUBSPOT_TOKEN env var."""
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        return {"connected": False, "error": "HUBSPOT_TOKEN not set in environment"}

    url = "https://api.hubapi.com/crm/v3/objects/deals?limit=1"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=headers)

        if r.status_code == 200:
            data = r.json()
            return {"connected": True, "status_code": r.status_code, "sample": data}
        else:
            return {"connected": False, "status_code": r.status_code, "detail": r.text}
    except Exception as e:
        return {"connected": False, "error": str(e)}
