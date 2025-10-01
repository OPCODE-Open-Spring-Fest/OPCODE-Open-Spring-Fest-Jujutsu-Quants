# app/adk/orchestrator.py - COMPLETE FIXED VERSION

# CRITICAL: Warning suppression MUST be at the very top, before any other imports
import os
import warnings
import logging

# Environment variables for GRPC and logging
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Suppress all warnings
warnings.filterwarnings('ignore')

# Configure logging to suppress lower-level messages
logging.getLogger('google').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)
logging.getLogger('google.cloud').setLevel(logging.ERROR)
logging.getLogger('google.generativeai').setLevel(logging.ERROR)
logging.getLogger('vertexai').setLevel(logging.ERROR)
logging.getLogger('grpc').setLevel(logging.ERROR)
logging.basicConfig(level=logging.ERROR)

# Custom warning filter for Gemini-specific warnings
class GeminiWarningFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage() if hasattr(record, 'getMessage') else str(record)
        warning_patterns = [
            'Warning: there are non-text parts in the response',
            'non-text parts in the response',
            'returning concatenated text result from text parts',
            'Check the full candidates.content.parts accessor'
        ]
        return not any(pattern in message for pattern in warning_patterns)

# Apply filters
for logger_name in ['google', 'google.generativeai', 'vertexai', 'grpc', 'google.cloud']:
    logger = logging.getLogger(logger_name)
    logger.addFilter(GeminiWarningFilter())
    logger.setLevel(logging.ERROR)

# NOW import the rest normally
from typing import Dict, Any, List
import json
import asyncio
import re
import sys
from io import StringIO
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.adk.agents import (
    create_anomaly_detector, create_summarizer, create_diversity_analyzer, create_breaking_news_alert, create_bias_detector, create_news_qa_agent, create_sentiment_agent
)

class Orchestrator:
    def __init__(self):
        self.anomaly_detector = create_anomaly_detector()
        self.summarizer = create_summarizer()
        self.diversity_analyzer = create_diversity_analyzer()
        self.breaking_news_alert = create_breaking_news_alert()
        self.bias_detector = create_bias_detector()
        self.news_qa_agent = create_news_qa_agent()
        self.sentiment_agent = create_sentiment_agent()

    async def process_news_workflow(self, market_data, news_articles, question=None):
        results = {}
        # anomalies from anomaly_detector
        results['anomalies'] = self.anomaly_detector.detect(market_data)
        # summaries from summarizer
        results['summaries'] = self.summarizer.summarize(news_articles)
        # diversity from diversity_analyzer
        results['diversity'] = self.diversity_analyzer.analyze(news_articles)
        # breaking alerts from breaking_news_alert
        results['breaking_alerts'] = self.breaking_news_alert.alert(news_articles)
        # bias from bias_detector
        results['bias'] = self.bias_detector.detect(news_articles)
        # sentiment from sentiment_agent
        results['sentiment'] = self.sentiment_agent.analyze(news_articles)
        # optional QA
        if question:
            results['qa'] = self.news_qa_agent.answer(news_articles, question)
        return results

    def run_all_advanced(self, market_data, news_articles, question=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.process_news_workflow(market_data, news_articles, question))

# Global orchestrator instance
try:
    orchestrator = Orchestrator()
    print("🚀 TradeSage ADK Orchestrator (Clean Output Version) ready")
except Exception as e:
    print(f"❌ Failed to initialize TradeSage Orchestrator: {str(e)}")
    orchestrator = None
