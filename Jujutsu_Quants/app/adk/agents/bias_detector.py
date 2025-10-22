from app.config.adk_config import AGENT_CONFIGS
import re

BIAS_INSTRUCTION = """
You are the Contextual Bias Detector Agent. You identify bias by checking for strongly polarized language in proximity to target entities.
You will output a Bias Score (0 to 100) and a confidence level (Low, Medium, High).
Output format: JSON array of articles with detailed bias flags.
"""

# Polarity words that increase or decrease sentiment strength
POLARITY_LEXICON = {
    # High Positive:
    'triumph': 20, 'brilliant': 20, 'masterful': 20, 'unprecedented': 15, 'success': 15,
    # High Negative:
    'disaster': -20, 'catastrophe': -20, 'fiasco': -20, 'failure': -15, 'scandal': -15,
    # Medium or qualifying:
    'claims': 10, 'allegedly': 10, 'so-called': 10, 'must': 5, 'should': 5,
}

PROXIMITY_WINDOW = 10
MAX_CONTEXT_SCORE = 100


def create_bias_detector():
    config = AGENT_CONFIGS["bias_detector"]

    class BiasDetector:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = BIAS_INSTRUCTION
            self.tools = []

        def _analyze_contextual_bias(self, text, entity):
            """Check for polarized words near entity mentions."""
            words = re.findall(r'\b\w+\b', text.lower())
            entity_indices = [i for i, w in enumerate(words) if w == entity.lower()]
            contextual_score = 0

            for idx in entity_indices:
                start = max(0, idx - PROXIMITY_WINDOW)
                end = min(len(words), idx + PROXIMITY_WINDOW + 1)
                context = words[start:end]
                score = sum(POLARITY_LEXICON.get(word, 0) for word in context)
                contextual_score += abs(score)

            return contextual_score

        def detect(self, articles, entities=None):
            """Main bias detection method."""
            bias_results = []

            # Step 1️⃣ — Resolve entity list
            if entities is None:
                entities = config.get('entities', [])
                if not entities:
                    derived = []
                    for art in articles:
                        title = art.get('title', '')
                        found = re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", title)
                        derived.extend([x.lower() for x in found])
                    entities = list(set(derived))

            # Step 2️⃣ — Analyze each article
            for article in articles:
                text = article.get('content', '')
                if not text:
                    continue

                for entity in entities:
                    if entity.lower() in text.lower():
                        score = self._analyze_contextual_bias(text, entity)
                        if score > 0:
                            normalized = min(score, MAX_CONTEXT_SCORE)
                            if normalized >= 60:
                                conf = "High"
                            elif normalized >= 30:
                                conf = "Medium"
                            else:
                                conf = "Low"

                            bias_results.append({
                                "title": article.get("title", "Untitled"),
                                "entity_focus": entity.lower(),
                                "bias_score": normalized,
                                "confidence": conf,
                                "bias_flag": True,
                                "bias_type": "Contextual Sentiment/Framing",
                                "reason": f"Strongly polarized language detected near '{entity}'."
                            })
                            break  # stop after first match per article

            return bias_results

    return BiasDetector()
