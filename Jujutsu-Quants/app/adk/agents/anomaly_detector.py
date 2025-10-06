from app.config.adk_config import AGENT_CONFIGS

ANOMALY_INSTRUCTION = """
You are the Anomaly Detector Agent. Identify and report significant anomalies in market data.
Output format: JSON array of anomalies with details and a confidence score (0.0 to 1.0).
"""

# Define a higher threshold for 'high confidence'
HIGH_CONFIDENCE_THRESHOLD = 0.5 

def create_anomaly_detector():
    config = AGENT_CONFIGS["anomaly_detector"]
    class AnomalyDetector:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = ANOMALY_INSTRUCTION
            self.tools = []
        
        def _calculate_confidence(self, price_change):
            """
            Calculates a confidence ratio (0.0 to 1.0) based on the magnitude of the price change.
            Confidence is higher for more extreme price changes.
            """
            # Normalize the absolute change against a fixed 'maximum possible' or 'very high' change (e.g., 1.0)
            # Clip the value to a maximum of 1.0 to ensure the ratio is at most 1.0
            confidence = min(abs(price_change) / 0.5, 1.0) 
            return round(confidence, 3)
            
        def detect(self, market_data):
            anomalies = []
            
            # The base detection threshold remains 0.1
            DETECTION_THRESHOLD = 0.1
            
            for entry in market_data:
                price_change = entry.get('price_change', 0)
                
                # Check for the initial anomaly condition
                if abs(price_change) > DETECTION_THRESHOLD:
                    
                    # Calculate the confidence ratio
                    confidence_ratio = self._calculate_confidence(price_change)
                    
                    # Determine the confidence level description
                    if confidence_ratio >= HIGH_CONFIDENCE_THRESHOLD:
                        confidence_level = "High"
                    else:
                        confidence_level = "Medium"

                    anomalies.append({
                        "symbol": entry.get("symbol"),
                        "price_change": price_change,
                        "reason": "Significant price movement",
                        "confidence_ratio": confidence_ratio, # New field
                        "confidence_level": confidence_level  # New field
                    })
            return anomalies
    return AnomalyDetector()

# Example of how the confidence is calculated:
# If price_change is 0.1, confidence is 0.1/0.5 = 0.2 (Medium)
# If price_change is 0.25, confidence is 0.25/0.5 = 0.5 (High)
# If price_change is 0.7, confidence is min(0.7/0.5, 1.0) = 1.0 (High)