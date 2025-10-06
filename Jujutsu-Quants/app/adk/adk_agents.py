try:
    from google.adk.agents import Agent
except Exception:  # ADK optional
    Agent = None


def _safe_agent(name: str, description: str, instruction: str, model: str = "gemini-2.0-flash", temperature: float = 0.2):
    if Agent is None:
        return None
    return Agent(
        name=name,
        model=model,
        description=description,
        instruction=instruction,
        tools=[],
        temperature=temperature,
    )


def create_adk_anomaly_agent(model: str = "gemini-2.0-flash"):
    instr = "Identify significant market anomalies from provided changes. Output concise bullets."
    return _safe_agent("adk_anomaly", "Detect market anomalies", instr, model)


def create_adk_summarizer_agent(model: str = "gemini-2.0-flash"):
    instr = "Summarize the news items clearly and briefly."
    return _safe_agent("adk_summarizer", "Summarize articles", instr, model)


def create_adk_diversity_agent(model: str = "gemini-2.0-flash"):
    instr = "Comment on source diversity and potential concentration."
    return _safe_agent("adk_diversity", "Assess source diversity", instr, model)


def create_adk_breaking_agent(model: str = "gemini-2.0-flash"):
    instr = "Flag items that are breaking/urgent."
    return _safe_agent("adk_breaking", "Flag breaking news", instr, model)


def create_adk_bias_agent(model: str = "gemini-2.0-flash"):
    instr = "Note potential bias or loaded language if present."
    return _safe_agent("adk_bias", "Detect bias cues", instr, model)


def create_adk_sentiment_agent(model: str = "gemini-2.0-flash"):
    instr = "Classify overall sentiment (positive/negative/neutral) for each item."
    return _safe_agent("adk_sentiment", "Classify sentiment", instr, model)


def create_adk_qa_agent(model: str = "gemini-2.0-flash"):
    instr = "Answer the user question using only the provided news content."
    return _safe_agent("adk_qa", "Q&A over news", instr, model)
