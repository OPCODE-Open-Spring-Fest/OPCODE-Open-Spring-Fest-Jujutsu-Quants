from app.config.adk_config import AGENT_CONFIGS

BIAS_INSTRUCTION = """
You are the Bias Detector Agent. Detect and report potential bias in news coverage.
Output format: JSON array of articles with bias flags.
"""

def create_bias_detector():
    config = AGENT_CONFIGS["bias_detector"]
    class BiasDetector:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = BIAS_INSTRUCTION
            self.tools = []
        def detect(self, articles):
            bias_results = []
            for article in articles:
                text = article.get('content', '').lower()
                if 'always' in text or 'never' in text:
                    bias_results.append({'title': article.get('title', ''), 'bias': 'potential'})
            return bias_results
    return BiasDetector()
