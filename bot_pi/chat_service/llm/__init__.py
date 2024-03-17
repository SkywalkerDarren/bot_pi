from typing import Literal


def get_llm(name: Literal["openai", "claude"]):
    if name == "openai":
        from chat_service.llm.openai_engine import OpenAIEngine
        return OpenAIEngine()
    elif name == "claude":
        from chat_service.llm.claude_engine import ClaudeEngine
        return ClaudeEngine()
    else:
        raise ValueError(f"Unknown llm: {name}")
