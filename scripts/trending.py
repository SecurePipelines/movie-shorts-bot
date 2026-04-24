from pytrends.request import TrendReq
import random

def get_trending_topics():
    try:
        pytrends = TrendReq(hl='en-IN', tz=330)

        # Try real-time trending searches
        df = pytrends.realtime_trending_searches(pn='IN')
        topics = df[0].tolist()

        if topics:
            return topics[:5]

    except Exception as e:
        print("Pytrends failed:", e)

    # ✅ Fallback (VERY IMPORTANT)
    fallback_topics = [
        "latest Bollywood movie scene",
        "RRR emotional scene",
        "KGF action scene",
        "Pushpa dialogue",
        "top movie moments",
        "sad movie scene",
        "romantic movie clip",
        "best thriller scenes"
    ]

    return random.sample(fallback_topics, 5)