# ShareChat Trending Tags System

> APM Assignment — ShareChat Trending Tags Discovery System

**Live Demo:** https://tangerine-sprinkles-c6eb08.netlify.app/  
**GitHub Repo:** https://github.com/PRATHAMESH0810/sharechat-trending  
**Video Walkthrough:** https://loom.com/share/your-link-here

---

## 1. How the System Decides What's Trending

### Signal Sources & Weights

| Source | Weight | Why |
|--------|--------|-----|
| News APIs (RSS/Web) | 30% | Breaking news = highest authority |
| Social Media (X/Insta/SC) | 25% | Direct public conversation measure |
| Search Volume (Google/Internal) | 20% | Shows active user intent |
| Entertainment/OTT | 15% | Movies, sports = massive engagement |
| Cultural Calendar | 10% | Festivals create predictable spikes |

### Scoring Logic

```
Heat Score = [Weighted Signal Sum] x Recency x Engagement x 100

Recency Multiplier = 0.5^(hours/6)     [6-hour half-life]
Engagement Boost = (views + shares*2 + comments*3) / 100K
```

### Filters Applied
1. **Spam Detection** — Remove >80% bot engagement
2. **Diversity** — Max 3 tags/category in Top 10
3. **Min Threshold** — Heat > 50 to qualify
4. **Geo Relevance** — >30% signal from Indian sources
5. **Language** — Prioritize Hindi + regional

---

## 2. Pipeline Workflow Diagram

```
Raw Sources (News/Social/Search/Cultural)
         |
         v
Signal Ingestion (Kafka / 5-min batches)
         |
         v
NLP Processing (spaCy + IndicBERT)
  - Entity Extraction
  - Keyword Normalization
  - Topic Clustering (BERT, sim > 0.85)
  - Deduplication (Fuzzy Match)
         |
         v
Scoring Engine
  - Weighted Signal Sum
  - Recency Decay (6h half-life)
  - Engagement Boost
  - Quality Filters
         |
         v
Ranking & Deduplication
  - Diversity Enforcement
  - Geo Filter
  - Top 12 Final List
         |
         v
API Layer (Flask + Redis Cache)
         |
         v
Mobile App (Feed + Detail View)
```

---

## 3. Model/API/Technique Per Stage

| Stage | Tool/Model | Why This One |
|-------|-----------|--------------|
| **Ingestion** | Kafka Event Bus | Handles real-time streams, fault-tolerant |
| **NLP** | spaCy + IndicBERT | Best Hindi NER support, fast inference |
| **Clustering** | BERT Embeddings | Semantic similarity > keyword matching |
| **Deduplication** | Fuzzy Matching (Levenshtein < 3) | Catches typos, transliteration variants |
| **Scoring** | Custom Weighted Formula | Flexible, explainable, tunable |
| **API** | Flask + Redis | Lightweight, Python-native, 5-min cache TTL |
| **Frontend** | Vanilla JS + CSS | Zero build step, fastest prototype |

---

## 4. UX Rationale

### What We Optimized For
- **Glanceability** — Hero card + large rank numbers = top story in < 2 sec
- **Scannability** — Vertical list, consistent cards, color-coded categories
- **Depth on Demand** — Tap for detail; signal bars show WHY it's trending
- **Cultural Fit** — Hindi-first, regional context, cricket + festivals prominent

### What We Rejected
| Idea | Why Rejected |
|------|-------------|
| Horizontal carousel | Poor scanning; vertical = native mobile |
| Grid layout | Too dense; single column = readable |
| Auto-play videos | Data-heavy; India has variable networks |
| Infinite scroll | Trends are finite; pagination clearer |
| Tab categories | Pills = faster switch, no scroll loss |

---

## What We'd Build Next (4 More Weeks)

| Week | Focus |
|------|-------|
| **Week 1** | Real API integration (NewsAPI, Twitter, Google Trends) + Kafka streams |
| **Week 2** | Custom Hindi NER model + BERT topic clustering + sentiment analysis |
| **Week 3** | User personalization + location-based boosting + A/B testing |
| **Week 4** | WebSocket live updates + push notifications + analytics dashboard |

---

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** Vanilla JS + CSS (no build tools)
- **NLP:** spaCy + IndicBERT
- **Deployment:** Netlify Drop (frontend), Heroku (backend)

---
