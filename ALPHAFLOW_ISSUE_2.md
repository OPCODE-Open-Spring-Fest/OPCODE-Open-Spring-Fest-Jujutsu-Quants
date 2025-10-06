# Issue #2: 🧠 Fix News QA Agent Oversimplified Implementation

## 🎯 Problem Description
The `NewsQAAgent` in `app/adk/agents/news_qa_agent.py` has an extremely oversimplified implementation that only does basic keyword matching. This makes it completely inadequate for real-world question answering.

## 🔍 Current Problematic Code

### Lines 16-25 in `news_qa_agent.py`:
```python
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
```

## 🎯 Problems with Current Implementation

1. **Oversimplified Matching**: Only checks if any keyword exists in content
2. **No Relevance Scoring**: Doesn't rank articles by relevance to the question
3. **No Answer Extraction**: Returns entire article content instead of relevant excerpts
4. **No Context Understanding**: Doesn't understand question intent or context
5. **Poor User Experience**: Returns irrelevant or overly long responses

## 🎯 Required Fixes

### 1. Implement Relevance Scoring
Add proper relevance scoring to rank articles:

```python
def _calculate_relevance_score(self, article, question):
    """Calculate relevance score between article and question"""
    content = article.get('content', '').lower()
    title = article.get('title', '').lower()
    question_lower = question.lower()
    
    score = 0
    
    # Keyword matching with weights
    question_words = set(question_lower.split())
    content_words = set(content.split())
    title_words = set(title.split())
    
    # Title matches are more important
    title_matches = len(question_words.intersection(title_words))
    score += title_matches * 3
    
    # Content matches
    content_matches = len(question_words.intersection(content_words))
    score += content_matches * 1
    
    # Phrase matching (exact phrases are more relevant)
    for word in question_words:
        if word in content:
            score += 0.5
    
    return score

def _rank_articles_by_relevance(self, articles, question):
    """Rank articles by relevance to the question"""
    scored_articles = []
    
    for article in articles:
        score = self._calculate_relevance_score(article, question)
        if score > 0:  # Only include articles with some relevance
            scored_articles.append((article, score))
    
    # Sort by score (highest first)
    scored_articles.sort(key=lambda x: x[1], reverse=True)
    return [article for article, score in scored_articles]
```

### 2. Implement Answer Extraction
Extract relevant excerpts instead of returning entire articles:

```python
def _extract_relevant_excerpts(self, article, question, max_length=200):
    """Extract relevant excerpts from article based on question"""
    content = article.get('content', '')
    question_words = set(question.lower().split())
    
    # Split content into sentences
    sentences = content.split('. ')
    
    # Score each sentence based on keyword matches
    scored_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        matches = sum(1 for word in question_words if word in sentence_lower)
        if matches > 0:
            scored_sentences.append((sentence, matches))
    
    # Sort by relevance and take top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    
    # Build excerpt
    excerpt = ""
    for sentence, score in scored_sentences:
        if len(excerpt + sentence) < max_length:
            excerpt += sentence + ". "
        else:
            break
    
    return excerpt.strip()

def _generate_answer(self, articles, question):
    """Generate a comprehensive answer from multiple articles"""
    if not articles:
        return "No relevant articles found."
    
    # Get top 3 most relevant articles
    top_articles = articles[:3]
    
    answers = []
    for i, article in enumerate(top_articles):
        excerpt = self._extract_relevant_excerpts(article, question)
        if excerpt:
            source = f"Source {i+1}: {article.get('title', 'Untitled')}"
            answers.append(f"{source}\n{excerpt}")
    
    if not answers:
        return "No relevant information found in the articles."
    
    return "\n\n".join(answers)
```

### 3. Add Question Type Detection
Implement different handling for different question types:

```python
def _detect_question_type(self, question):
    """Detect the type of question being asked"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['what', 'how', 'why', 'when', 'where']):
        return 'factual'
    elif any(word in question_lower for word in ['compare', 'difference', 'vs', 'versus']):
        return 'comparative'
    elif any(word in question_lower for word in ['trend', 'change', 'over time', 'recently']):
        return 'temporal'
    elif any(word in question_lower for word in ['impact', 'effect', 'consequence']):
        return 'causal'
    else:
        return 'general'

def _handle_question_type(self, question, articles):
    """Handle different question types with appropriate strategies"""
    question_type = self._detect_question_type(question)
    
    if question_type == 'comparative':
        return self._handle_comparative_question(question, articles)
    elif question_type == 'temporal':
        return self._handle_temporal_question(question, articles)
    elif question_type == 'causal':
        return self._handle_causal_question(question, articles)
    else:
        return self._handle_general_question(question, articles)
```

### 4. Enhanced Answer Method
Replace the simple answer method with comprehensive implementation:

```python
def answer(self, articles, question):
    """Enhanced answer method with relevance scoring and answer extraction"""
    if not articles or not question:
        return {'answer': 'No articles or question provided.'}
    
    # Rank articles by relevance
    relevant_articles = self._rank_articles_by_relevance(articles, question)
    
    if not relevant_articles:
        return {'answer': 'No relevant articles found for this question.'}
    
    # Generate answer based on question type
    answer_text = self._handle_question_type(question, relevant_articles)
    
    # Get source information
    sources = [article.get('title', 'Untitled') for article in relevant_articles[:3]]
    
    return {
        'answer': answer_text,
        'sources': sources,
        'relevance_score': self._calculate_relevance_score(relevant_articles[0], question),
        'question_type': self._detect_question_type(question)
    }
```

## 🧪 Test Cases to Implement

```python
def test_relevance_scoring():
    """Test relevance scoring functionality"""
    agent = create_news_qa_agent()
    
    articles = [
        {
            'title': 'Apple Reports Strong Earnings',
            'content': 'Apple Inc. reported strong quarterly earnings, beating analyst expectations.'
        },
        {
            'title': 'Market Update',
            'content': 'The stock market showed mixed signals today.'
        }
    ]
    
    question = "What did Apple report about earnings?"
    
    # Test relevance scoring
    score1 = agent._calculate_relevance_score(articles[0], question)
    score2 = agent._calculate_relevance_score(articles[1], question)
    
    assert score1 > score2  # Apple article should be more relevant

def test_answer_extraction():
    """Test answer extraction from articles"""
    agent = create_news_qa_agent()
    
    article = {
        'title': 'Apple Reports Strong Earnings',
        'content': 'Apple Inc. reported strong quarterly earnings, beating analyst expectations. The company saw significant growth in iPhone sales. Revenue increased by 15% compared to last year.'
    }
    
    question = "What did Apple report about earnings?"
    excerpt = agent._extract_relevant_excerpts(article, question)
    
    assert 'earnings' in excerpt.lower()
    assert len(excerpt) < 200  # Should be truncated

def test_question_type_detection():
    """Test question type detection"""
    agent = create_news_qa_agent()
    
    assert agent._detect_question_type("What is Apple's revenue?") == 'factual'
    assert agent._detect_question_type("Compare Apple and Microsoft") == 'comparative'
    assert agent._detect_question_type("How has the market changed recently?") == 'temporal'

def test_enhanced_answer():
    """Test enhanced answer method"""
    agent = create_news_qa_agent()
    
    articles = [
        {
            'title': 'Apple Reports Strong Earnings',
            'content': 'Apple Inc. reported strong quarterly earnings, beating analyst expectations.'
        }
    ]
    
    question = "What did Apple report about earnings?"
    result = agent.answer(articles, question)
    
    assert 'answer' in result
    assert 'sources' in result
    assert 'relevance_score' in result
    assert 'question_type' in result
    assert 'earnings' in result['answer'].lower()
```

## 📁 Files to Modify
- `app/adk/agents/news_qa_agent.py` (main fix)
- `tests/test_news_qa_agent.py` (new test file)

## ✅ Acceptance Criteria
- [ ] Relevance scoring implemented
- [ ] Answer extraction from articles added
- [ ] Question type detection implemented
- [ ] Enhanced answer method with comprehensive responses
- [ ] Source attribution added
- [ ] Unit tests cover all new functionality
- [ ] Documentation updated with new features

## 🏷️ Labels
`enhancement`, `nlp`, `question-answering`, `good first issue`

## 💡 Implementation Hints
- Use TF-IDF or similar techniques for better relevance scoring
- Consider using sentence transformers for semantic similarity
- Implement caching for frequently asked questions
- Add configuration options for answer length and number of sources

---
**Difficulty**: Intermediate  
**Estimated Time**: 4-5 hours  
**Skills**: Python, NLP, Text Processing, Question Answering
