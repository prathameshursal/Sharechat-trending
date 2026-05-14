# 🚀 Deployment Guide

## Quick Start (2 minutes)

### Option 1: Deploy Frontend to Vercel (Recommended)
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel --prod

# 3. Get your URL
# Example: https://sharechat-trending-demo.vercel.app
```

### Option 2: Deploy Frontend to Netlify
```bash
# 1. Install Netlify CLI
npm i -g netlify-cli

# 2. Deploy
netlify deploy --prod --dir .

# 3. Get your URL
# Example: https://sharechat-trending-demo.netlify.app
```

### Option 3: Deploy Frontend to GitHub Pages
```bash
# 1. Push to GitHub
gh repo create sharechat-trending --public --source=. --push

# 2. Enable GitHub Pages in repo settings
# Settings → Pages → Source: main branch

# 3. Access at
# https://yourusername.github.io/sharechat-trending/
```

### Option 4: Run Locally
```bash
# Frontend
python -m http.server 3000
# Open http://localhost:3000

# Backend (separate terminal)
cd backend
pip install -r requirements.txt
python app.py
# API at http://localhost:5000
```

---

## Backend Deployment (Heroku)

```bash
# 1. Install Heroku CLI
brew install heroku  # macOS
# or download from heroku.com

# 2. Login
heroku login

# 3. Create app
heroku create sharechat-trending-api

# 4. Deploy
git subtree push --prefix backend heroku main

# 5. Verify
heroku open
```

---

## Environment Variables

Create a `.env` file in backend/:
```
FLASK_ENV=production
PORT=5000
NEWS_API_KEY=your_newsapi_key
TWITTER_BEARER_TOKEN=your_twitter_token
GOOGLE_TRENDS_API_KEY=your_google_key
REDIS_URL=redis://localhost:6379
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trending` | GET | List trending tags |
| `/api/trending/<tag>` | GET | Trend detail |
| `/api/categories` | GET | List categories |
| `/api/health` | GET | Health check |

### Example Request
```bash
curl https://your-api.herokuapp.com/api/trending
```

### Example Response
```json
{
  "success": true,
  "timestamp": "2026-05-05T06:52:00",
  "total": 12,
  "trends": [
    {
      "rank": 1,
      "tag": "#पश्चिमबंगालचुनाव",
      "hindi_tag": "#पश्चिमबंगालचुनाव",
      "description": "बीजेपी ने पश्चिम बंगाल में ऐतिहासिक जीत दर्ज की",
      "category": "राजनीति",
      "heat_score": 98.5,
      "heat_label": "🔥🔥🔥",
      "sources": ["news", "social", "search"],
      "source_breakdown": {
        "news": 35, "social": 30, "search": 25,
        "entertainment": 0, "cultural": 0
      },
      "engagement": {
        "views": 5200000,
        "shares": 890000,
        "comments": 450000
      },
      "recency_hours": 2,
      "related_posts": 154000,
      "location": "पश्चिम बंगाल, भारत",
      "icon": "🔴",
      "color": "#FF4444"
    }
  ]
}
```

---

## Testing the Prototype

1. **Open the deployed URL** on your phone
2. **Verify** you see 12 trending tags
3. **Tap** on #1 trend (West Bengal elections)
4. **Check** detail view with AI summary and signal breakdown
5. **Scroll** through related posts
6. **Filter** by category (Politics → Sports → Entertainment)
7. **Search** for "IPL" or "बंगाल"
8. **Pull down** to refresh (on mobile)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API not responding | Check Heroku logs: `heroku logs --tail` |
| CORS errors | Ensure `flask-cors` is installed |
| Fonts not loading | Check internet connection (Google Fonts CDN) |
| Mobile layout broken | Ensure viewport meta tag is present |
| Trends not updating | Clear cache or check API health endpoint |

---

## Submission Checklist

- [ ] Hosted prototype URL (Vercel/Netlify)
- [ ] GitHub repository URL
- [ ] 2-minute Loom video walkthrough
- [ ] Screenshot of trending tags list
- [ ] README with system design
- [ ] Pipeline diagram

---

*Built for ShareChat APM Assignment | May 2026*
