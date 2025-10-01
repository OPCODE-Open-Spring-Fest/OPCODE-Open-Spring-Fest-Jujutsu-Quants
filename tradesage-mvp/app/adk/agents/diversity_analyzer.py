from app.config.adk_config import AGENT_CONFIGS

DIVERSITY_INSTRUCTION = """
You are the Diversity Analyzer Agent. Analyze the diversity of news sources in the provided articles.
Output format: JSON object with source counts.
"""

def create_diversity_analyzer():
    config = AGENT_CONFIGS["diversity_analyzer"]
    class DiversityAnalyzer:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = DIVERSITY_INSTRUCTION
            self.tools = []
        def analyze(self, articles):
            source_count = {}
            for article in articles:
                source = article.get('source', 'unknown')
                source_count[source] = source_count.get(source, 0) + 1
            return source_count
    return DiversityAnalyzer()
