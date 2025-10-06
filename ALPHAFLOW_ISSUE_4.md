# Issue #4: 🔧 Fix Agent Integration and Error Handling

## 🎯 Problem Description
The agent integration in the orchestrator has several issues including poor error handling, inconsistent return formats, and lack of proper validation. This makes the system unreliable and difficult to debug.

## 🔍 Current Problems

### 1. Inconsistent Return Formats
Different agents return different data structures, making integration difficult:

```python
# Bias detector returns complex objects
bias_results.append({
    'title': article.get('title', 'Untitled'),
    'entity_focus': entity,
    'bias_score': normalized_score,
    'confidence': confidence,
    'bias_flag': True,
    'bias_type': "Contextual Sentiment/Framing",
    'reason': f"Strongly polarized language detected near '{entity}'."
})

# Sentiment agent returns simple objects
results.append({
    "title": a.get("title", ""),
    "sentiment": sentiment
})

# News QA agent returns different format
return {
    'title': article.get('title', ''),
    'answer': article.get('content', '')
}
```

### 2. No Error Handling in Orchestrator
The orchestrator doesn't handle agent failures gracefully:

```python
async def _process_lightweight(self, market_data, news_articles, question=None):
    results = {}
    results['anomalies'] = self.anomaly_detector.detect(market_data)  # ❌ No error handling
    results['summaries'] = self.summarizer.summarize(news_articles)  # ❌ No error handling
    results['diversity'] = self.diversity_analyzer.analyze(news_articles)  # ❌ No error handling
    # ... more agents without error handling
```

### 3. No Input Validation
Agents don't validate their inputs, leading to runtime errors:

```python
def detect(self, articles):
    bias_results = []
    
    for article in articles:  # ❌ No validation that articles is a list
        text = article.get('content', '')  # ❌ No validation that article is a dict
        if not text:
            continue
        # ... rest of processing
```

## 🎯 Required Fixes

### 1. Implement Standardized Agent Interface
Create a standard interface that all agents must implement:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

class BaseAgent(ABC):
    """Base class for all agents with standardized interface"""
    
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "unknown")
        self.model = config.get("model", "unknown")
        self.description = config.get("description", "")
        self.instruction = config.get("instruction", "")
        self.tools = []
        self.logger = logging.getLogger(f"agent.{self.name}")
    
    @abstractmethod
    def process(self, data: Any) -> Dict[str, Any]:
        """Process data and return standardized result"""
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data"""
        return True
    
    def handle_error(self, error: Exception, data: Any) -> Dict[str, Any]:
        """Handle errors gracefully"""
        self.logger.error(f"Error processing data: {error}")
        return {
            "status": "error",
            "error": str(error),
            "data": data,
            "agent": self.name
        }
    
    def get_standard_result(self, status: str, data: Any, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Get standardized result format"""
        result = {
            "status": status,
            "agent": self.name,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        if metadata:
            result["metadata"] = metadata
        return result
```

### 2. Implement Error Handling in Orchestrator
Add comprehensive error handling to the orchestrator:

```python
async def _process_lightweight(self, market_data, news_articles, question=None):
    """Process workflow with comprehensive error handling"""
    results = {}
    
    # Define agent processing tasks
    agent_tasks = [
        ("anomalies", self.anomaly_detector, market_data),
        ("summaries", self.summarizer, news_articles),
        ("diversity", self.diversity_analyzer, news_articles),
        ("breaking_alerts", self.breaking_news_alert, news_articles),
        ("bias", self.bias_detector, news_articles),
        ("sentiment", self.sentiment_agent, news_articles),
    ]
    
    # Add QA agent if question provided
    if question:
        agent_tasks.append(("qa", self.news_qa_agent, (news_articles, question)))
    
    # Process each agent with error handling
    for result_key, agent, data in agent_tasks:
        try:
            # Validate input
            if not agent.validate_input(data):
                results[result_key] = agent.get_standard_result(
                    "error", 
                    data, 
                    {"error": "Invalid input data"}
                )
                continue
            
            # Process data
            if result_key == "qa":
                articles, q = data
                result = agent.answer(articles, q)
            else:
                result = agent.process(data)
            
            # Standardize result
            if isinstance(result, dict) and "status" in result:
                results[result_key] = result
            else:
                results[result_key] = agent.get_standard_result("success", result)
                
        except Exception as e:
            self.logger.error(f"Error processing {result_key}: {e}")
            results[result_key] = agent.handle_error(e, data)
    
    return results
```

### 3. Add Input Validation to All Agents
Implement proper input validation:

```python
def validate_input(self, data: Any) -> bool:
    """Validate input data for bias detector"""
    if not isinstance(data, list):
        self.logger.error("Bias detector expects a list of articles")
        return False
    
    for i, article in enumerate(data):
        if not isinstance(article, dict):
            self.logger.error(f"Article {i} is not a dictionary")
            return False
        
        if 'content' not in article:
            self.logger.warning(f"Article {i} missing 'content' field")
    
    return True

def process(self, articles: List[Dict]) -> Dict[str, Any]:
    """Process articles with error handling"""
    try:
        if not self.validate_input(articles):
            return self.get_standard_result("error", articles, {"error": "Invalid input"})
        
        # Process articles
        bias_results = self.detect(articles)
        
        return self.get_standard_result("success", bias_results, {
            "articles_processed": len(articles),
            "bias_detected": len(bias_results)
        })
        
    except Exception as e:
        return self.handle_error(e, articles)
```

### 4. Implement Agent Health Monitoring
Add health monitoring for agents:

```python
class AgentHealthMonitor:
    """Monitor agent health and performance"""
    
    def __init__(self):
        self.agent_stats = {}
        self.logger = logging.getLogger("agent_monitor")
    
    def record_agent_execution(self, agent_name: str, success: bool, execution_time: float):
        """Record agent execution statistics"""
        if agent_name not in self.agent_stats:
            self.agent_stats[agent_name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "average_execution_time": 0,
                "last_execution": None
            }
        
        stats = self.agent_stats[agent_name]
        stats["total_executions"] += 1
        stats["last_execution"] = datetime.utcnow().isoformat()
        
        if success:
            stats["successful_executions"] += 1
        else:
            stats["failed_executions"] += 1
        
        # Update average execution time
        stats["average_execution_time"] = (
            (stats["average_execution_time"] * (stats["total_executions"] - 1) + execution_time) 
            / stats["total_executions"]
        )
    
    def get_agent_health(self, agent_name: str) -> Dict[str, Any]:
        """Get health status for an agent"""
        if agent_name not in self.agent_stats:
            return {"status": "unknown", "message": "No execution history"}
        
        stats = self.agent_stats[agent_name]
        success_rate = stats["successful_executions"] / stats["total_executions"]
        
        if success_rate >= 0.9:
            status = "healthy"
        elif success_rate >= 0.7:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return {
            "status": status,
            "success_rate": success_rate,
            "total_executions": stats["total_executions"],
            "average_execution_time": stats["average_execution_time"],
            "last_execution": stats["last_execution"]
        }
```

## 🧪 Test Cases to Implement

```python
def test_agent_input_validation():
    """Test agent input validation"""
    agent = create_bias_detector()
    
    # Test invalid input
    assert not agent.validate_input("not a list")
    assert not agent.validate_input([{"invalid": "article"}])
    
    # Test valid input
    valid_articles = [{"content": "Test article", "title": "Test"}]
    assert agent.validate_input(valid_articles)

def test_agent_error_handling():
    """Test agent error handling"""
    agent = create_bias_detector()
    
    # Test with invalid data
    result = agent.process("invalid data")
    
    assert result["status"] == "error"
    assert "error" in result
    assert result["agent"] == agent.name

def test_orchestrator_error_handling():
    """Test orchestrator error handling"""
    orchestrator = Orchestrator()
    
    # Test with invalid data
    result = await orchestrator._process_lightweight("invalid", "invalid")
    
    assert "anomalies" in result
    assert result["anomalies"]["status"] == "error"

def test_agent_health_monitoring():
    """Test agent health monitoring"""
    monitor = AgentHealthMonitor()
    
    # Record some executions
    monitor.record_agent_execution("bias_detector", True, 0.5)
    monitor.record_agent_execution("bias_detector", False, 0.3)
    monitor.record_agent_execution("bias_detector", True, 0.4)
    
    health = monitor.get_agent_health("bias_detector")
    
    assert health["status"] == "degraded"  # 2/3 success rate
    assert health["success_rate"] == 2/3
    assert health["total_executions"] == 3
```

## 📁 Files to Modify
- `app/adk/agents/base_agent.py` (new file)
- `app/adk/agents/bias_detector.py` (update to inherit from BaseAgent)
- `app/adk/agents/sentiment_agent.py` (update to inherit from BaseAgent)
- `app/adk/agents/news_qa_agent.py` (update to inherit from BaseAgent)
- `app/adk/orchestrator.py` (add error handling)
- `tests/test_agent_integration.py` (new test file)

## ✅ Acceptance Criteria
- [ ] Standardized agent interface implemented
- [ ] All agents inherit from BaseAgent
- [ ] Comprehensive error handling in orchestrator
- [ ] Input validation for all agents
- [ ] Agent health monitoring implemented
- [ ] Consistent return formats across all agents
- [ ] Unit tests cover all error scenarios
- [ ] Documentation updated with new architecture

## 🏷️ Labels
`bug`, `enhancement`, `architecture`, `error-handling`, `integration`, `good first issue`

## 💡 Implementation Hints
- Use abstract base classes for consistent interfaces
- Implement retry logic for transient failures
- Add metrics collection for monitoring
- Consider using dependency injection for better testability

---
**Difficulty**: Intermediate  
**Estimated Time**: 5-6 hours  
**Skills**: Python, OOP, Error Handling, Architecture, Testing
