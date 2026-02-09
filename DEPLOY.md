# Vercel Deployment Guide

## 🚀 Quick Deploy Backend

```bash
cd backend
vercel --prod
```

When prompted:
- **Project name**: `revenue-ai-agent`
- **Framework**: Python
- **Root directory**: `./`

## 🔐 Set Environment Variables in Vercel

After deployment, go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**

Add these secrets:
```
OPENAI_API_KEY=sk-proj-...
HUBSPOT_TOKEN=pat-na2-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL=C0ADUC4CL9J
GOOGLE_CREDENTIALS_FILE=/tmp/gsa-key.json
```

### For Google Sheets:
1. Upload `gsa-key.json` to Vercel as a file-based secret (or use environment variable with JSON content)
2. Or set `GOOGLE_SERVICE_ACCOUNT_JSON` with the full JSON content

## 🎨 Quick Deploy Frontend

```bash
cd frontend
vercel --prod
```

Update your frontend's `vite.config.js` to point to the deployed backend:

```javascript
proxy: {
  '/api': {
    target: 'https://your-backend.vercel.app',
    changeOrigin: true
  }
}
```

## 📡 After Deployment

Backend URL: `https://your-backend.vercel.app`
Frontend URL: `https://your-frontend.vercel.app`

Test backend:
```
https://your-backend.vercel.app/api/status
```

## ⚠️ Common Issues

**Google Sheets not syncing?**
- Vercel has `/tmp` read-only access
- Use `GOOGLE_SERVICE_ACCOUNT_JSON` env var with JSON content instead of file path

**Module not found errors?**
- Ensure all modules (ai_scoring.py, crm_integration.py, etc.) are in backend/ directory
- Check `backend/requirements.txt` has all dependencies

**CORS errors?**
- Frontend URL must be added to CORS in `main.py`
- Update `allow_origins` in `app.add_middleware(CORSMiddleware, ...)`
