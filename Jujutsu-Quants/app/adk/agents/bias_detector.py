from app.config.adk_config import AGENT_CONFIGS
import re

BIAS_INSTRUCTION = """
You are the Contextual Bias Detector Agent. You identify bias by checking for strongly polarized language in proximity to target entities.
You will output a Bias Score (0 to 100) and a confidence level (Low, Medium, High).
Output format: JSON array of articles with detailed bias flags.
"""

# 1. Define High-Impact Polarity Lexicon (Words that strongly swing sentiment)
POLARITY_LEXICON = {
    # High Positive:
    'triumph': 20, 'brilliant': 20, 'masterful': 20, 'unprecedented': 15, 'success': 15,
    # High Negative:
    'disaster': -20, 'catastrophe': -20, 'fiasco': -20, 'failure': -15, 'scandal': -15,
    # Medium/Qualifying Language (adds to tone score):
    'claims': 10, 'allegedly': 10, 'so-called': 10, 'must': 5, 'should': 5,
}

# 2. Define Target Entities and a Proximity Window
TARGET_ENTITIES = [
    "company_x", 
    "politician_y", 
    "policy_z"
]

# The window size (number of words) to check before and after the entity.
PROXIMITY_WINDOW = 10 

# Max score for normalization
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
            """
            Checks for polarized words within a small window of the target entity.
            Returns a cumulative contextual bias score.
            """
            raw_text = text.lower()
            
            # Use regex to split the text into words while preserving word boundaries
            words = re.findall(r'\b\w+\b', raw_text)
            
            # Find all indices where the entity appears
            entity_indices = [i for i, word in enumerate(words) if word == entity]
            
            contextual_score = 0
            
            for entity_index in entity_indices:
                # Define the context window
                start = max(0, entity_index - PROXIMITY_WINDOW)
                end = min(len(words), entity_index + PROXIMITY_WINDOW + 1)
                
                context = words[start:end]
                
                # Calculate the score within this specific context
                context_polarity = 0
                for word in context:
                    context_polarity += POLARITY_LEXICON.get(word, 0)
                
                # Add the absolute score to the total. We are looking for *any* strong polarization.
                contextual_score += abs(context_polarity) 
                
            return contextual_score

        def detect(self, articles):
            bias_results = []
            
            for article in articles:
                text = article.get('content', '')
                if not text:
                    continue
                
                detected_bias = False
                
                for entity in TARGET_ENTITIES:
                    # Check if the entity is present in the article
                    if entity in text.lower():
                        
                        # 1. Calculate the contextual bias score
                        raw_score = self._analyze_contextual_bias(text, entity)
                        
                        if raw_score > 0:
                            # 2. Normalize and assign confidence
                            normalized_score = min(raw_score, MAX_CONTEXT_SCORE)
                            
                            # Simple rule for confidence:
                            if normalized_score >= 60:
                                confidence = "High"
                            elif normalized_score >= 30:
                                confidence = "Medium"
                            else:
                                confidence = "Low"
                            
                            bias_results.append({
                                'title': article.get('title', 'Untitled'),
                                'entity_focus': entity,
                                'bias_score': normalized_score,
                                'confidence': confidence,
                                'bias_flag': True,
                                'bias_type': "Contextual Sentiment/Framing",
                                'reason': f"Strongly polarized language detected near '{entity}'."
                            })
                            
                            detected_bias = True
                            # Once bias is detected for any entity, move to the next article
                            break 
                            
            return bias_results
    return BiasDetector()