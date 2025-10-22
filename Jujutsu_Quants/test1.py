import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from Jujutsu_Quants.app.adk.agents.bias_detector import create_bias_detector





articles = [
    {
        "title": "Tesla beats expectations in Q4",
        "content": "Analysts say Tesla showed unprecedented growth and triumph this quarter."
    },
    {
        "title": "Tesla faces scandal over autopilot safety",
        "content": "Critics claim Tesla’s failure to address issues has caused a disaster in its reputation."
    }
]

det = create_bias_detector()
output = det.detect(articles, entities=["Tesla"])

print("\n🧠 Bias Detection Output:")
for item in output:
    print(f"- Title: {item['title']}")
    print(f"  Entity: {item['entity_focus']}")
    print(f"  Bias Score: {item['bias_score']} ({item['confidence']})")
    print(f"  Reason: {item['reason']}\n")
