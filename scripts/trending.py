from pytrends.request import TrendReq

def get_trending_topics():
    pytrends = TrendReq()
    trends = pytrends.trending_searches(pn='india')
    return trends[0].tolist()[:5]