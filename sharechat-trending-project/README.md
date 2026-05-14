# 🔥 ShareChat Trending Tags System

> APM Assignment — ShareChat Trending Tags Discovery System & Mobile App Prototype

**Live Demo:** [Open Prototype](https://sharechat-trending-demo.vercel.app) *(Deploy to any static host)*  
**Backend API:** [API Docs](http://localhost:5000/) *(Run locally)*  
**Video Walkthrough:** [Loom Link](https://loom.com/share/your-link-here) *(Record after review)*

---

## 📋 Assignment Overview

This project delivers a complete end-to-end solution for ShareChat's Trending Tags feature:

1. **Trending Tags System** — Multi-signal algorithm that identifies, scores, and ranks what's trending in India
2. **Mobile App Prototype** — Clickable, mobile-native UI with feed, detail views, and real-time data
3. **AI-Generated Summaries** — Context-aware summaries for each trend (Bonus)
4. **Documentation** — System design, UX rationale, and roadmap

---

## 🏗️ System Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRENDING TAGS PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│  │ News APIs   │   │ Social Media│   │ Search Data │   │ Cultural    │   │
│  │ (RSS/Web)   │   │ (X/Insta/   │   │ (Google/    │   │ Calendar    │   │
│  │             │   │ ShareChat)  │   │ Internal)   │   │             │   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   │
│         │                 │                 │                 │          │
│         └─────────────────┴─────────────────┴─────────────────┘          │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  Signal Ingestion │  ← Kafka / Event Bus              │
│                    │  (Real-time)      │                                    │
│                    └─────────┬─────────┘                                    │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  NLP Processing   │  ← spaCy / IndicBERT              │
│                    │  (Hindi/English)  │    Entity Extraction               │
│                    │  Topic Clustering │    Keyword Normalization           │
│                    └─────────┬─────────┘                                    │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  Scoring Engine   │  ← Custom Algorithm                 │
│                    │  (Heat Score)     │    Weighted Multi-signal            │
│                    │  Recency Decay    │    Diversity Enforcement             │
│                    │  Quality Filter   │    Spam Detection                  │
│                    └─────────┬─────────┘                                    │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  Ranking &        │  ← Top N Selection                 │
│                    │  Deduplication    │    Category Balance                │
│                    └─────────┬─────────┘                                    │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  API Layer        │  ← REST/JSON                       │
│                    │  (Flask/FastAPI)  │    Caching (Redis)                   │
│                    └─────────┬─────────┘                                    │
│                              │                                              │
│                    ┌─────────▼─────────┐                                    │
│                    │  Mobile App       │  ← React/Vanilla JS                │
│                    │  (Feed + Detail)  │    Real-time Updates                 │
│                    └─────────────────┘                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Scoring Algorithm

### Signal Weights

| Signal Source | Weight | Rationale |
|--------------|--------|-----------|
| **News APIs** | 30% | Breaking news has highest authority for "what India is talking about" |
| **Social Media** | 25% | Direct measure of public conversation and virality |
| **Search Volume** | 20% | Indicates active user intent and curiosity |
| **Entertainment** | 15% | OTT releases, sports events drive massive engagement |
| **Cultural Calendar** | 10% | Festivals create predictable but important spikes |

### Heat Score Formula

```
Heat Score = [Σ(Signal_i × Weight_i)] × Recency_Multiplier × Engagement_Multiplier × 100

Where:
- Signal_i = Normalized signal strength (0-1)
- Weight_i = Source weight from table above
- Recency_Multiplier = 0.5^(hours_since_peak / 6)  [6-hour half-life]
- Engagement_Multiplier = min(1 + (views + shares×2 + comments×3) / 100000, 3.0)
```

### Quality Filters

1. **Spam Detection**: Remove tags with >80% bot-like engagement patterns
2. **Diversity Enforcement**: Max 3 tags from same category in Top 10
3. **Minimum Threshold**: Heat score > 50 to appear in feed
4. **Geographic Relevance**: Must have >30% signal from Indian sources
5. **Language Filter**: Prioritize Hindi + regional language content

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python) — Lightweight, fast to prototype
- **NLP**: spaCy + IndicBERT for Hindi entity extraction
- **Data Sources**: NewsAPI, Twitter API v2, Google Trends, Internal ShareChat analytics
- **Caching**: Redis (optional) for 5-minute trend caching
- **Deployment**: Heroku / AWS Lambda / GCP Cloud Run

### Frontend
- **Framework**: Vanilla JavaScript (no build step needed)
- **Styling**: CSS3 with CSS Variables for theming
- **Mobile-First**: 430px max-width container, touch-optimized
- **Animations**: CSS transitions + keyframes for smooth UX
- **Hosting**: Vercel / Netlify / GitHub Pages

---

## 📱 UX Design Rationale

### What We Optimized For

1. **Glanceability**: Users should understand the top story in < 2 seconds
   - Hero card for #1 trend with large typography
   - Heat score prominently displayed
   - Emoji + color coding for instant category recognition

2. **Scannability**: Quick vertical scan to find interesting topics
   - Clear rank numbers (1, 2, 3...)
   - Consistent card layout
   - Category pills for filtering

3. **Depth on Demand**: Tap to explore without overwhelming the feed
   - Detail view slides up (mobile-native pattern)
   - Signal breakdown shows "why this is trending"
   - AI summary provides context without reading 10 articles

4. **Cultural Fit**: Designed for Hindi-speaking Indian users
   - All content in Hindi (Devanagari script)
   - Regional context (state-specific trends)
   - Festival and cricket prominently featured

### What We Considered and Rejected

| Alternative | Why Rejected |
|------------|-------------|
| Horizontal carousel | Poor for scanning; vertical scroll is native mobile behavior |
| Grid layout | Too dense; single-column cards better for readability |
| Auto-playing videos | Data-heavy; India has variable network quality |
| Infinite scroll | Trends are finite (Top 12); pagination clearer |
| Dark mode default | ShareChat brand is bright/energetic; light mode fits better |
| Tab-based categories | Pills allow faster switching without losing scroll position |

---

## 🚀 How to Run

### Backend (Local)
```bash
cd backend
pip install -r requirements.txt
python app.py
# API runs on http://localhost:5000
```

### Frontend (Local)
```bash
cd frontend
# Open index.html in browser or serve with:
python -m http.server 3000
# Open http://localhost:3000
```

### Deploy to Vercel (Frontend)
```bash
npm i -g vercel
vercel --prod
```

### Deploy to Heroku (Backend)
```bash
heroku create sharechat-trending-api
heroku git:remote -a sharechat-trending-api
git subtree push --prefix backend heroku main
```

---

## 📊 Sample API Response

```json
{
  "success": true,
  "timestamp": "2026-05-05T06:52:00",
  "total": 12,
  "trends": [
    {
      "rank": 1,
      "tag": "#पश्चिमबंगालचुनाव",
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

## 🗺️ What We'd Build Next (4 Weeks)

### Week 1: Real Data Integration
- Connect to actual NewsAPI, Twitter API v2, Google Trends
- Implement Kafka stream for real-time ingestion
- Add Redis caching layer

### Week 2: ML Improvements
- Train custom Hindi NER model on ShareChat content
- Implement topic clustering with BERT embeddings
- Add sentiment analysis for trend quality scoring

### Week 3: Personalization
- User interest profiling based on past engagement
- Location-based trend boosting (state-level trends)
- A/B testing framework for ranking algorithms

### Week 4: Scale & Polish
- Add WebSocket support for live updates
- Implement push notifications for breaking trends
- Analytics dashboard for content team
- Accessibility improvements (screen reader support)

---

## 📝 Data Sources & Assumptions

### Real Data Used (May 5, 2026)
- **West Bengal Election Results**: BJP historic win, Mamata Banerjee loses [^12^][^13^]
- **Tamil Nadu Elections**: Actor Vijay's political debut [^1^]
- **Buddha Purnima**: Cultural festival trending [^9^]
- **IPL 2026**: Cricket season ongoing [^4^]
- **LPG Price Hike**: Commercial cylinder rate increase [^7^]
- **Vaishali Chess**: Vaishali Rameshbabu wins Candidates [^5^]

### Assumptions (Where Data Unavailable)
1. **Engagement metrics**: Estimated based on typical ShareChat post performance for similar topics
2. **Heat scores**: Calculated using our scoring formula with estimated signal strengths
3. **Social signals**: Approximated from Twitter/Google Trends patterns
4. **Related content**: Mock posts representative of actual user-generated content

---

## 🎥 Video Walkthrough

[Record 2-minute Loom showing:]
1. Opening the app and seeing trending feed
2. Tapping on #1 trend (West Bengal elections)
3. Showing detail view with AI summary and signal breakdown
4. Scrolling through related posts
5. Filtering by category (Sports → Entertainment)
6. Explaining the pipeline diagram

---

## 👨‍💻 Built With

- **Claude 3.5 Sonnet** — Code generation, system design, documentation
- **Cursor IDE** — Frontend development assistance
- **Flask** — Backend API framework
- **Vanilla JS + CSS** — Frontend (no build tools for rapid prototyping)

---

## 📄 License

MIT License — Built for ShareChat APM Assignment

---

*Last updated: May 5, 2026*
