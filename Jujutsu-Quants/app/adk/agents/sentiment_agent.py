from app.config.adk_config import AGENT_CONFIGS
from typing import List, Dict

SENTIMENT_INSTRUCTION = """
You are the Sentiment Agent. Classify each article as positive, negative, or neutral based on content.
Output format: list of {title, sentiment}.
"""

def create_sentiment_agent():
    # Reuse summarizer/bias config if needed; add default
    config = AGENT_CONFIGS.get("sentiment_agent", {
        "name": "sentiment_agent",
        "model": "rule_based",
        "description": "Heuristic sentiment classifier"
    })

    class SentimentAgent:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = SENTIMENT_INSTRUCTION
            self.tools: List = []
            self.positive_words = {
                "beat", "beats", "surge", "surges", "growth", "strong", "record", "gain", "gains",
                "improve", "improves", "improved", "up", "rise", "rises", "bullish", "positive"
            }
            self.negative_words = {
                "miss", "falls", "drop", "drops", "decline", "declines", "weak", "loss", "losses",
                "cut", "cuts", "down", "bearish", "negative", "pressure", "warning", "warns"
            }
        def classify(self, text: str) -> str:
            if not text:
                return "neutral"
            t = text.lower()
            pos = sum(1 for w in self.positive_words if w in t)
            neg = sum(1 for w in self.negative_words if w in t)
            if pos > neg:
                return "positive"
            if neg > pos:
                return "negative"
            return "neutral"
        def classify_with_confidence(self, text: str) -> Dict[str, Any]:
            """Classify text with confidence and reason."""
            t = text.lower() if text else ""
            pos_count = sum(1 for w in self.positive_words if w in t)
            neg_count = sum(1 for w in self.negative_words if w in t)
            label = self.classify(text)
            confidence = min(1.0, (pos_count + neg_count) / 5.0)  # capped at 1.0
            reason = f"pos={pos_count}, neg={neg_count}"
            return {
                "label": label,
                "confidence": confidence,
                "reason": reason
            }
        def analyze(self, articles: List[Dict]) -> List[Dict]:
            results: List[Dict] = []
            for a in articles:
                sentiment = self.classify(a.get("content", ""))
                results.append({
                    "title": a.get("title", ""),
                    "sentiment": sentiment
                })
            return results
    return SentimentAgent()
