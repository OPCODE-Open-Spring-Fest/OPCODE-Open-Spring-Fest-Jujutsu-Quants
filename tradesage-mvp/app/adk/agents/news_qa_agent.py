from app.config.adk_config import AGENT_CONFIGS

QA_INSTRUCTION = """
You are the News QA Agent. Answer user questions using the news corpus. Be concise and cite the article title in your answer. If no answer is found, say 'No relevant article found.'
"""

def create_news_qa_agent():
    config = AGENT_CONFIGS["news_qa_agent"]
    class NewsQAAgent:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = QA_INSTRUCTION
            self.tools = []
        def answer(self, articles, question):
            keywords = question.lower().split() if question else []
            for article in articles:
                content = article.get('content', '').lower()
                if any(word in content for word in keywords):
                    return {
                        'title': article.get('title', ''),
                        'answer': article.get('content', '')
                    }
            return {'answer': 'No relevant article found.'}
    return NewsQAAgent()
