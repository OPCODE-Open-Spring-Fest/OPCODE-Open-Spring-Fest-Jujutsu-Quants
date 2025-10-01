from app.config.adk_config import AGENT_CONFIGS

ANOMALY_INSTRUCTION = """
You are the Anomaly Detector Agent. Identify and report significant anomalies in market data.
Output format: JSON array of anomalies with details.
"""

def create_anomaly_detector():
    config = AGENT_CONFIGS["anomaly_detector"]
    class AnomalyDetector:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = ANOMALY_INSTRUCTION
            self.tools = []
        def detect(self, market_data):
            anomalies = []
            for entry in market_data:
                if abs(entry.get('price_change', 0)) > 0.1:
                    anomalies.append({
                        "symbol": entry.get("symbol"),
                        "price_change": entry.get("price_change"),
                        "reason": "Significant price movement"
                    })
            return anomalies
    return AnomalyDetector()
