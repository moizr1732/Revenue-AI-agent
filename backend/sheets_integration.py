"""Google Sheets Integration Module"""
import os
import json
import gspread
from typing import Dict, Any, List


def get_google_client():
    """Authenticate and return gspread client."""
    svc_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE")

    if svc_json:
        info = json.loads(svc_json)
        return gspread.service_account_from_dict(info)
    elif creds_file and os.path.exists(creds_file):
        return gspread.service_account(filename=creds_file)
    else:
        raise Exception("Google service account credentials not provided (set GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_CREDENTIALS_FILE)")


async def sync_deals_to_sheets(sheet_id: str, deals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Sync analyzed deals to Google Sheet."""
    if not sheet_id:
        return {"synced": False, "error": "sheet_id is required"}

    try:
        gc = get_google_client()
        sh = gc.open_by_key(sheet_id)
        ws = sh.sheet1
        
        # Prepare rows with analyzed data
        rows = [["deal_id", "deal_name", "amount", "stage", "risk_score", "risk_reason", "timestamp"]]
        for deal in deals:
            rows.append([
                deal.get("deal_id"),
                deal.get("deal_name"),
                deal.get("amount"),
                deal.get("stage"),
                deal.get("risk_score"),
                deal.get("risk_reason"),
                deal.get("timestamp")
            ])
        
        ws.clear()
        ws.update(rows)
        return {"synced": True, "rows_written": len(rows)-1}
    except Exception as e:
        return {"synced": False, "error": str(e)}


async def read_sheets(sheet_id: str, range_name: str = None) -> Dict[str, Any]:
    """Read rows from Google Sheet."""
    if not sheet_id:
        return {"error": "sheet_id is required"}

    try:
        gc = get_google_client()
        sh = gc.open_by_key(sheet_id)
        ws = sh.sheet1

        if range_name:
            values = ws.get(range_name)
        else:
            values = ws.get_all_values()

        return {"sheet_id": sheet_id, "rows": values}
    except Exception as e:
        return {"error": str(e)}
