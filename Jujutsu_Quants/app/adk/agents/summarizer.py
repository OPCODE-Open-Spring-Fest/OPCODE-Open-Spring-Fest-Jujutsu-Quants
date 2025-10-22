from app.config.adk_config import AGENT_CONFIGS

SUMMARIZER_INSTRUCTION = """
You are the News Summarizer Agent. Summarize news articles concisely and clearly.
Output format: JSON array of summaries with article titles.
"""

def create_summarizer():
    config = AGENT_CONFIGS["summarizer"]
    class NewsSummarizer:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = SUMMARIZER_INSTRUCTION
            self.tools = []
        def summarize(self, articles):
            summaries = []
            for article in articles:
                text = article.get('content', '')
                summary = text[:150] + '...' if len(text) > 150 else text
                summaries.append({'title': article.get('title', ''), 'summary': summary})
            return summaries
    return NewsSummarizer()
