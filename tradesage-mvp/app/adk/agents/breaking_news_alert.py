from app.config.adk_config import AGENT_CONFIGS

BREAKING_ALERT_INSTRUCTION = """
You are the Breaking News Alert Agent. Flag and report breaking news articles.
Output format: JSON array of flagged articles.
"""

def create_breaking_news_alert():
    config = AGENT_CONFIGS["breaking_news_alert"]
    class BreakingNewsAlert:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = BREAKING_ALERT_INSTRUCTION
            self.tools = []
        def alert(self, articles):
            alerts = []
            for article in articles:
                if 'breaking' in article.get('title', '').lower():
                    alerts.append(article)
            return alerts
    return BreakingNewsAlert()
