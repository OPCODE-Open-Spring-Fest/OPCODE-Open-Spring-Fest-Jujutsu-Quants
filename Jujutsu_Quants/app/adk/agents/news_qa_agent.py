import re
import math
from collections import Counter
from typing import List, Dict, Any, TypedDict, Union

from app.config.adk_config import AGENT_CONFIGS

# --- Type Definitions for API Contract ---

class Passage(TypedDict):
    text: str
    source: str
    start: int
    end: int

class Citation(TypedDict):
    source: str
    start: int
    end: int

class RankedPassage(TypedDict):
    """Cleaner type for ranked results."""
    passage: Passage
    score: float

class Answer(TypedDict):
    answer: str
    citations: List[Citation]

# --- Default Constants ---

DEFAULT_CHUNK_SIZE = 150
DEFAULT_CHUNK_OVERLAP = 30
DEFAULT_TOP_K = 3
DEFAULT_MIN_SCORE = 0.05

# --- Agent Instruction ---

QA_INSTRUCTION = """
You are the News QA Agent. Answer user questions using the news corpus.
Be concise and cite the article title or URL. If no answer is found, say 'No relevant article found.'
"""

# --- Factory Function ---

def create_news_qa_agent():
    config = AGENT_CONFIGS["news_qa_agent"]

    class NewsQAAgent:
        def __init__(self):
            self.name = config["name"]
            self.model = config["model"]
            self.description = config["description"]
            self.instruction = QA_INSTRUCTION
            self.tools = []

        def answer(
            self,
            articles: List[Dict[str, Any]],
            question: str,
            top_k: int = DEFAULT_TOP_K,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
            overlap: int = DEFAULT_CHUNK_OVERLAP,
            min_score: float = DEFAULT_MIN_SCORE
        ) -> Answer:
            """
            Returns an extractive answer with citations from a list of articles.
            """
            fallback_answer = "No relevant article found."
            passages: List[Passage] = []
            top_passages: List[RankedPassage] = []

            if articles:
                # 1. Chunk articles into passages
                passages = _chunk_articles(articles, chunk_size, overlap)
            
            if passages:
                # 2. Rank passages
                ranked_passages = _rank_passages(passages, question)
                top_passages = [
                    r for r in ranked_passages[:top_k] if r['score'] > min_score
                ]

            # 3. Compose answer & collect citations (or return fallback)
            if not top_passages:
                return {"answer": fallback_answer, "citations": []}

            final_answer = " ".join([r['passage']['text'] for r in top_passages])
            final_citations: List[Citation] = [
                {
                    "source": r['passage']['source'],
                    "start": r['passage']['start'],
                    "end": r['passage']['end']
                } for r in top_passages
            ]

            return {"answer": final_answer, "citations": final_citations}

    return NewsQAAgent()

# --- Helper Functions ---

def _chunk_articles(
    articles: List[Dict[str, Any]],
    chunk_size: int,
    overlap: int
) -> List[Passage]:
    """
    Splits articles into overlapping passages.
    Returns a list of Passage dicts with text, source, start, end.
    """
    passages: List[Passage] = []

    for article in articles:
        content = article.get('content', '')
        if not content.strip():
            continue
        source = article.get('source_url', article.get('title', 'unknown_source'))

        words = list(re.finditer(r'\S+', content))
        if not words:
            continue

        start_idx = 0
        while start_idx < len(words):
            end_idx = min(start_idx + chunk_size, len(words))
            
            if start_idx >= end_idx:
                break
                
            start_char = words[start_idx].start()
            end_char = words[end_idx - 1].end()
            passage_text = content[start_char:end_char]

            passages.append({
                "text": passage_text,
                "source": source,
                "start": start_char,
                "end": end_char
            })

            # Safe step to prevent infinite loop even if overlap >= chunk_size
            next_start_idx = start_idx + chunk_size - overlap
            start_idx = max(next_start_idx, start_idx + 1)

    return passages

def _rank_passages(passages: List[Passage], question: str) -> List[RankedPassage]:
    """
    Ranks passages by TF-IDF cosine similarity to the question.
    Returns list of RankedPassage dicts.
    """
    passage_texts = [p['text'] for p in passages]
    passage_tokens = [_tokenize(t) for t in passage_texts]
    question_tokens = _tokenize(question)

    corpus_tokens = passage_tokens + [question_tokens]
    idf_scores = _compute_idf(corpus_tokens)
    vocab = sorted(idf_scores.keys())

    question_vector = _compute_tfidf_vector(question_tokens, idf_scores, vocab)

    ranked: List[RankedPassage] = []
    for p_tokens, p in zip(passage_tokens, passages):
        passage_vector = _compute_tfidf_vector(p_tokens, idf_scores, vocab)
        score = _cosine_similarity(question_vector, passage_vector)
        ranked.append({"passage": p, "score": score})

    return sorted(ranked, key=lambda x: x['score'], reverse=True)

# --- TF-IDF & Cosine Helpers ---

def _tokenize(text: str) -> List[str]:
    return re.findall(r'\w+', text.lower())

def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    return {w: c / total for w, c in counts.items()}

def _compute_idf(documents: List[List[str]]) -> Dict[str, float]:
    num_docs = len(documents)
    if num_docs == 0:
        return {}
    df = Counter()
    for doc in documents:
        df.update(set(doc))
    return {w: math.log(num_docs / (1 + count)) + 1 for w, count in df.items()}

def _compute_tfidf_vector(tokens: List[str], idf_scores: Dict[str, float], vocab: List[str]) -> List[float]:
    tf = _compute_tf(tokens)
    return [tf.get(word, 0) * idf_scores.get(word, 0) for word in vocab]

def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity using math.hypot for efficiency."""
    dot_product = sum(a*b for a, b in zip(vec1, vec2))
    mag1 = math.hypot(*vec1)
    mag2 = math.hypot(*vec2)
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)



# --- Testing ---


# if __name__ == "__main__":
#     # Create agent instance
#     agent = create_news_qa_agent()  # fixed: create the agent

#     # Sample articles
#     articles = [
#         {
#             "source_url": "https://news.example.com/1",
#             "title": "Tesla announces new Model X",
#             "content": "Tesla announced the new Model X electric SUV. Production will start next year."
#         },
#         {
#             "source_url": "https://news.example.com/2",
#             "title": "Stock Market Today",
#             "content": "NASDAQ and S&P 500 both increased today due to tech stock rally."
#         }
#     ]

#     # Sample question
#     question = "What did Tesla announce?"

#     # Get answer
#     result = agent.answer(articles, question)  # fixed: use .answer method

#     # Print result
#     print("Answer:", result["answer"])
#     print("Citations:", result["citations"])
