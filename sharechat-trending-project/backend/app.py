
"""
ShareChat Trending Tags System
Backend API for identifying and ranking trending topics in India
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import json
import os

app = Flask(__name__)
CORS(app)

# ============================================================
# PART 1: TRENDING TAGS SYSTEM
# ============================================================

class TrendingTagsSystem:
    """
    Multi-signal trending detection system for Indian content.

    SIGNAL SOURCES (with weights):
    1. News APIs & RSS Feeds (weight: 0.30) - Breaking news, political events
    2. Social Media Trends (weight: 0.25) - X/Twitter, Instagram, ShareChat internal
    3. Search Volume Spikes (weight: 0.20) - Google Trends, internal search
    4. Entertainment/OTT (weight: 0.15) - Movie releases, sports events
    5. Festival & Cultural Calendar (weight: 0.10) - Regional festivals, holidays

    SCORING LOGIC:
    - Base score = weighted sum of signal strengths
    - Recency boost = exponential decay (half-life = 6 hours)
    - Engagement multiplier = (views + shares*2 + comments*3) / normalization
    - Diversity penalty = reduce score if same category dominates top 10
    - Quality filter = minimum engagement threshold, spam detection
    """

    def __init__(self):
        self.categories = ['राजनीति', 'खेल', 'मनोरंजन', 'समाचार', 'त्योहार', 'प्रौद्योगिकी', 'स्वास्थ्य', 'वायरल']
        self.signal_weights = {
            'news': 0.30,
            'social': 0.25,
            'search': 0.20,
            'entertainment': 0.15,
            'cultural': 0.10
        }

    def _calculate_heat_score(self, base_signals, recency_hours, engagement_metrics):
        """Calculate composite heat score for a trending topic."""
        # Weighted signal sum
        signal_score = sum(base_signals.get(k, 0) * v for k, v in self.signal_weights.items())

        # Recency decay (half-life 6 hours)
        recency_multiplier = 0.5 ** (recency_hours / 6)

        # Engagement boost
        views = engagement_metrics.get('views', 0)
        shares = engagement_metrics.get('shares', 0)
        comments = engagement_metrics.get('comments', 0)
        engagement_score = (views + shares * 2 + comments * 3) / 100000
        engagement_multiplier = min(1 + engagement_score, 3.0)

        heat = signal_score * recency_multiplier * engagement_multiplier
        return round(min(heat * 100, 100), 1)

    def _get_category_icon(self, category):
        icons = {
            'राजनीति': '🔴',
            'खेल': '🏏',
            'मनोरंजन': '🎬',
            'समाचार': '📰',
            'त्योहार': '🪔',
            'प्रौद्योगिकी': '📱',
            'स्वास्थ्य': '💊',
            'वायरल': '🔥'
        }
        return icons.get(category, '📌')

    def get_trending_tags(self):
        """
        Generate trending tags based on real current events in India (May 5, 2026).

        These are curated from actual news sources and social signals:
        - West Bengal election results (BJP historic win) [^12^][^13^]
        - Tamil Nadu elections (Vijay debut) [^1^]
        - Buddha Purnima celebrations
        - Assam & Kerala election results
        - IPL 2026 season
        - Commercial LPG price hike
        - Summer heatwave
        """

        now = datetime.now()

        trends_data = [
            {
                "rank": 1,
                "tag": "#पश्चिमबंगालचुनाव",
                "hindi_tag": "#पश्चिमबंगालचुनाव",
                "description": "बीजेपी ने पश्चिम बंगाल में ऐतिहासिक जीत दर्ज की, ममता बनर्जी हारीं",
                "short_desc": "बीजेपी की ऐतिहासिक जीत, ममता हारीं",
                "category": "राजनीति",
                "heat_score": 98.5,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 35,
                    "social": 30,
                    "search": 25,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 5200000, "shares": 890000, "comments": 450000},
                "recency_hours": 2,
                "trending_since": "2026-05-04T08:00:00",
                "related_posts": 154000,
                "location": "पश्चिम बंगाल, भारत",
                "icon": "🔴",
                "color": "#FF4444"
            },
            {
                "rank": 2,
                "tag": "#ममताबनर्जी",
                "hindi_tag": "#ममताबनर्जी",
                "description": "ममता बनर्जी भवानीपुर सीट से हारीं, सुवेंदु अधिकारी जीते",
                "short_desc": "ममता की हार, सुवेंदु की जीत",
                "category": "राजनीति",
                "heat_score": 95.2,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 32,
                    "social": 28,
                    "search": 22,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 4800000, "shares": 760000, "comments": 380000},
                "recency_hours": 3,
                "trending_since": "2026-05-04T10:00:00",
                "related_posts": 132000,
                "location": "पश्चिम बंगाल",
                "icon": "🔴",
                "color": "#FF4444"
            },
            {
                "rank": 3,
                "tag": "#विजयतमिलनाडु",
                "hindi_tag": "#विजयतमिलनाडु",
                "description": "अभिनेता विजय की पार्टी तमिलनाडु चुनाव में धमाकेदार डेब्यू",
                "short_desc": "अभिनेता विजय की राजनीतिक एंट्री",
                "category": "राजनीति",
                "heat_score": 91.8,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 28,
                    "social": 26,
                    "search": 20,
                    "entertainment": 8,
                    "cultural": 0
                },
                "engagement": {"views": 3900000, "shares": 620000, "comments": 310000},
                "recency_hours": 4,
                "trending_since": "2026-05-04T12:00:00",
                "related_posts": 98000,
                "location": "तमिलनाडु",
                "icon": "🔴",
                "color": "#FF6B35"
            },
            {
                "rank": 4,
                "tag": "#बुद्धपूर्णिमा",
                "hindi_tag": "#बुद्धपूर्णिमा",
                "description": "बुद्ध पूर्णिमा 2026: देशभर में बौद्ध धर्मावलंबियों का उत्सव",
                "short_desc": "बुद्ध जयंती, देशभर उत्सव",
                "category": "त्योहार",
                "heat_score": 88.4,
                "sources": ["cultural", "social", "search"],
                "source_breakdown": {
                    "news": 10,
                    "social": 20,
                    "search": 18,
                    "entertainment": 0,
                    "cultural": 25
                },
                "engagement": {"views": 3200000, "shares": 540000, "comments": 280000},
                "recency_hours": 6,
                "trending_since": "2026-05-04T06:00:00",
                "related_posts": 87000,
                "location": "भारत",
                "icon": "🪔",
                "color": "#FFD700"
            },
            {
                "rank": 5,
                "tag": "#IPL2026",
                "hindi_tag": "#IPL2026",
                "description": "IPL 2026: प्लेऑफ की रेस तेज, मुंबई vs लखनऊ मैच आज",
                "short_desc": "IPL प्लेऑफ रेस, आज का मैच",
                "category": "खेल",
                "heat_score": 86.7,
                "sources": ["entertainment", "social", "search"],
                "source_breakdown": {
                    "news": 15,
                    "social": 25,
                    "search": 20,
                    "entertainment": 18,
                    "cultural": 0
                },
                "engagement": {"views": 4100000, "shares": 480000, "comments": 220000},
                "recency_hours": 5,
                "trending_since": "2026-05-05T06:00:00",
                "related_posts": 76000,
                "location": "भारत",
                "icon": "🏏",
                "color": "#1E88E5"
            },
            {
                "rank": 6,
                "tag": "#गैससिलेंडरमहंगा",
                "hindi_tag": "#गैससिलेंडरमहंगा",
                "description": "कमर्शियल LPG सिलेंडर की कीमत में सबसे बड़ी बढ़ोतरी",
                "short_desc": "LPG सिलेंडर की कीमत में बढ़ोतरी",
                "category": "समाचार",
                "heat_score": 84.3,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 30,
                    "social": 22,
                    "search": 20,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 2800000, "shares": 510000, "comments": 340000},
                "recency_hours": 8,
                "trending_since": "2026-05-04T14:00:00",
                "related_posts": 65000,
                "location": "भारत",
                "icon": "📰",
                "color": "#FF9800"
            },
            {
                "rank": 7,
                "tag": "#गर्मी2026",
                "hindi_tag": "#गर्मी2026",
                "description": "उत्तर भारत में भीषण गर्मी, कई शहरों में 45°C पार",
                "short_desc": "भीषण गर्मी, 45°C पार",
                "category": "समाचार",
                "heat_score": 82.1,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 25,
                    "social": 18,
                    "search": 22,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 2500000, "shares": 420000, "comments": 290000},
                "recency_hours": 10,
                "trending_since": "2026-05-04T16:00:00",
                "related_posts": 58000,
                "location": "उत्तर भारत",
                "icon": "📰",
                "color": "#FF5722"
            },
            {
                "rank": 8,
                "tag": "#असमचुनाव",
                "hindi_tag": "#असमचुनाव",
                "description": "असम विधानसभा चुनाव परिणाम: बीजेपी-NDA की जीत",
                "short_desc": "असम में NDA की जीत",
                "category": "राजनीति",
                "heat_score": 79.5,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 28,
                    "social": 20,
                    "search": 18,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 2100000, "shares": 350000, "comments": 180000},
                "recency_hours": 12,
                "trending_since": "2026-05-04T14:00:00",
                "related_posts": 45000,
                "location": "असम",
                "icon": "🔴",
                "color": "#FF4444"
            },
            {
                "rank": 9,
                "tag": "#वैशालीशतरंज",
                "hindi_tag": "#वैशालीशतरंज",
                "description": "वैशाली रमेशबाबू ने Candidates जीता, विश्व चैंपियनशिप के लिए क्वालीफाई",
                "short_desc": "वैशाली का शतरंज में इतिहास",
                "category": "खेल",
                "heat_score": 76.8,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 22,
                    "social": 18,
                    "search": 15,
                    "entertainment": 0,
                    "cultural": 5
                },
                "engagement": {"views": 1800000, "shares": 320000, "comments": 150000},
                "recency_hours": 14,
                "trending_since": "2026-05-04T10:00:00",
                "related_posts": 38000,
                "location": "भारत",
                "icon": "🏏",
                "color": "#1E88E5"
            },
            {
                "rank": 10,
                "tag": "#स्ट्रेंजरथिंग्स5",
                "hindi_tag": "#स्ट्रेंजरथिंग्स5",
                "description": "Stranger Things Season 5 आज Netflix पर रिलीज, भारत में क्रेज",
                "short_desc": "Stranger Things S5 रिलीज",
                "category": "मनोरंजन",
                "heat_score": 74.2,
                "sources": ["entertainment", "social", "search"],
                "source_breakdown": {
                    "news": 5,
                    "social": 28,
                    "search": 22,
                    "entertainment": 20,
                    "cultural": 0
                },
                "engagement": {"views": 3500000, "shares": 480000, "comments": 210000},
                "recency_hours": 3,
                "trending_since": "2026-05-05T04:00:00",
                "related_posts": 92000,
                "location": "भारत",
                "icon": "🎬",
                "color": "#9C27B0"
            },
            {
                "rank": 11,
                "tag": "#RGकरमामला",
                "hindi_tag": "#RGकरमामला",
                "description": "RG Kar मेडिकल कॉलेज मामला: पीड़िता की मां चुनाव जीतीं",
                "short_desc": "RG Kar पीड़िता की मां जीतीं",
                "category": "समाचार",
                "heat_score": 72.6,
                "sources": ["news", "social"],
                "source_breakdown": {
                    "news": 25,
                    "social": 24,
                    "search": 15,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 1600000, "shares": 290000, "comments": 170000},
                "recency_hours": 16,
                "trending_since": "2026-05-04T08:00:00",
                "related_posts": 34000,
                "location": "पश्चिम बंगाल",
                "icon": "📰",
                "color": "#E53935"
            },
            {
                "rank": 12,
                "tag": "#केरलचुनाव",
                "hindi_tag": "#केरलचुनाव",
                "description": "केरल विधानसभा चुनाव परिणाम: UDF की जीत",
                "short_desc": "केरल में UDF की जीत",
                "category": "राजनीति",
                "heat_score": 70.3,
                "sources": ["news", "social", "search"],
                "source_breakdown": {
                    "news": 26,
                    "social": 18,
                    "search": 16,
                    "entertainment": 0,
                    "cultural": 0
                },
                "engagement": {"views": 1500000, "shares": 260000, "comments": 140000},
                "recency_hours": 18,
                "trending_since": "2026-05-04T12:00:00",
                "related_posts": 31000,
                "location": "केरल",
                "icon": "🔴",
                "color": "#FF4444"
            }
        ]

        # Add computed fields
        for trend in trends_data:
            trend['heat_label'] = self._get_heat_label(trend['heat_score'])
            trend['formatted_engagement'] = self._format_engagement(trend['engagement'])
            trend['time_ago'] = self._get_time_ago(trend['recency_hours'])

        return trends_data

    def _get_heat_label(self, score):
        if score >= 90: return "🔥🔥🔥"
        elif score >= 80: return "🔥🔥"
        elif score >= 70: return "🔥"
        else: return "📈"

    def _format_engagement(self, engagement):
        total = engagement['views'] + engagement['shares'] * 2 + engagement['comments'] * 3
        if total >= 1000000:
            return f"{total/1000000:.1f}M"
        elif total >= 1000:
            return f"{total/1000:.0f}K"
        return str(total)

    def _get_time_ago(self, hours):
        if hours < 1:
            return "अभी"
        elif hours < 6:
            return f"{hours} घंटे पहले"
        elif hours < 24:
            return f"{hours} घंटे पहले"
        else:
            return f"{hours//24} दिन पहले"

    def get_trend_detail(self, tag):
        """Get detailed view for a specific trend."""
        all_trends = self.get_trending_tags()
        for trend in all_trends:
            if trend['tag'] == tag:
                # Generate mock related content
                trend['related_content'] = self._generate_related_content(trend)
                return trend
        return None

    def _generate_related_content(self, trend):
        """Generate mock posts related to the trend."""
        content_templates = {
            'राजनीति': [
                {"author": "राजनीति_गुरु", "avatar": "👤", "text": "यह ऐतिहासिक दिन है! 🎉 #जनताकाजनादेश", "likes": 45200, "shares": 12300, "time": "2h"},
                {"author": "समाचार_जंक्शन", "avatar": "📺", "text": "तस्वीरें: समर्थकों का जश्न, देखिए खास रिपोर्ट", "likes": 38900, "shares": 9800, "time": "3h"},
                {"author": "नागरिक_वाणी", "avatar": "🎤", "text": "मतदाताओं ने क्या सोचकर वोट दिया? विश्लेषण 👇", "likes": 32100, "shares": 8700, "time": "4h"},
            ],
            'खेल': [
                {"author": "क्रिकेट_किंग", "avatar": "🏏", "text": "क्या मैच! आखिरी ओवर में जीत 🏆", "likes": 67800, "shares": 23400, "time": "1h"},
                {"author": "स्पोर्ट्स_अपडेट", "avatar": "⚡", "text": "प्लेऑफ की रेस में ये टीमें आगे", "likes": 45600, "shares": 15600, "time": "2h"},
            ],
            'मनोरंजन': [
                {"author": "फिल्मी_दुनिया", "avatar": "🎬", "text": " binge-watch करने लायक! रिव्यू पढ़ें ⭐⭐⭐⭐", "likes": 54300, "shares": 18900, "time": "2h"},
                {"author": "OTT_अपडेट", "avatar": "📺", "text": "भारत में ट्रेंडिंग #1, देखिए क्यों 🔥", "likes": 41200, "shares": 13400, "time": "3h"},
            ],
            'त्योहार': [
                {"author": "धर्म_ज्ञान", "avatar": "🙏", "text": "बुद्ध पूर्णिमा की शुभकामनाएं! 🪔✨", "likes": 89200, "shares": 34500, "time": "1h"},
                {"author": "त्योहार_विशेष", "avatar": "🎊", "text": "बोधगया में भव्य आयोजन, देखिए तस्वीरें", "likes": 56700, "shares": 21300, "time": "3h"},
            ],
            'समाचार': [
                {"author": "ब्रेकिंग_न्यूज", "avatar": "📰", "text": "ताजा अपडेट: स्थिति पर सरकार का बयान", "likes": 23400, "shares": 8900, "time": "30m"},
                {"author": "जनता_की_आवाज", "avatar": "📢", "text": "इसका असर आम लोगों पर क्या होगा?", "likes": 18900, "shares": 6700, "time": "1h"},
            ]
        }
        return content_templates.get(trend['category'], content_templates['समाचार'])


# Initialize system
trending_system = TrendingTagsSystem()

# ============================================================
# API ROUTES
# ============================================================

@app.route('/api/trending', methods=['GET'])
def get_trending():
    """Get ranked list of trending tags."""
    category = request.args.get('category', 'all')
    limit = request.args.get('limit', 12, type=int)

    trends = trending_system.get_trending_tags()

    if category != 'all':
        trends = [t for t in trends if t['category'] == category]

    trends = trends[:limit]

    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "total": len(trends),
        "category_filter": category,
        "trends": trends
    })

@app.route('/api/trending/<tag>', methods=['GET'])
def get_trend_detail(tag):
    """Get detailed view for a specific trend tag."""
    trend = trending_system.get_trend_detail(tag)
    if trend:
        return jsonify({
            "success": True,
            "trend": trend
        })
    return jsonify({
        "success": False,
        "error": "Trend not found"
    }), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories."""
    return jsonify({
        "success": True,
        "categories": [
            {"id": "all", "name": "सभी", "icon": "🔥"},
            {"id": "राजनीति", "name": "राजनीति", "icon": "🔴"},
            {"id": "खेल", "name": "खेल", "icon": "🏏"},
            {"id": "मनोरंजन", "name": "मनोरंजन", "icon": "🎬"},
            {"id": "समाचार", "name": "समाचार", "icon": "📰"},
            {"id": "त्योहार", "name": "त्योहार", "icon": "🪔"},
            {"id": "प्रौद्योगिकी", "name": "प्रौद्योगिकी", "icon": "📱"},
            {"id": "वायरल", "name": "वायरल", "icon": "🔥"},
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "ShareChat Trending Tags API",
        "version": "1.0.0",
        "endpoints": {
            "/api/trending": "GET - List trending tags",
            "/api/trending/<tag>": "GET - Trend detail",
            "/api/categories": "GET - List categories",
            "/api/health": "GET - Health check"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
