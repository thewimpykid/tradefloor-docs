from langchain_core.messages import HumanMessage, RemoveMessage

# Import tools from separate utility files
from tradingagents.agents.utils.core_stock_tools import (
    get_stock_data
)
from tradingagents.agents.utils.technical_indicators_tools import (
    get_indicators
)
from tradingagents.agents.utils.fundamental_data_tools import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement
)
from tradingagents.agents.utils.news_data_tools import (
    get_news,
    get_insider_transactions,
    get_global_news
)


def get_language_instruction() -> str:
    """Return a prompt instruction for the configured output language.

    Returns empty string when English (default), so no extra tokens are used.
    Only applied to user-facing agents (analysts, portfolio manager).
    Internal debate agents stay in English for reasoning quality.
    """
    from tradingagents.dataflows.config import get_config
    lang = get_config().get("output_language", "English")
    if lang.strip().lower() == "english":
        return ""
    return f" Write your entire response in {lang}."


_TIMEFRAME_CONTEXT = {
    "short": (
        "Investment timeframe: SHORT-TERM (days to weeks). "
        "Prioritise momentum, technical indicators, near-term catalysts, and price action over long-run fundamentals."
    ),
    "medium": (
        "Investment timeframe: MEDIUM-TERM (weeks to months). "
        "Balance technical signals with fundamental factors; consider earnings cycles and sector trends."
    ),
    "long": (
        "Investment timeframe: LONG-TERM (months to years). "
        "Prioritise fundamentals, competitive moats, earnings growth trajectory, and intrinsic valuation over short-term noise."
    ),
}

_FOCUS_CONTEXT = {
    "fundamentals": (
        "Analysis focus: FUNDAMENTALS. "
        "Emphasise earnings quality, revenue growth, margins, balance sheet strength, valuation multiples, and competitive position."
    ),
    "technical": (
        "Analysis focus: TECHNICAL. "
        "Emphasise price action, chart patterns, volume trends, momentum indicators, and key support/resistance levels."
    ),
    "sentiment": (
        "Analysis focus: SENTIMENT. "
        "Emphasise news flow, social media sentiment, analyst revisions, insider transactions, and market psychology."
    ),
}


def build_instrument_context(ticker: str) -> str:
    """Describe the exact instrument and inject timeframe/focus context for all agents."""
    from tradingagents.dataflows.config import get_config
    cfg = get_config()

    parts = [
        f"The instrument to analyze is `{ticker}`. "
        "Use this exact ticker in every tool call, report, and recommendation, "
        "preserving any exchange suffix (e.g. `.TO`, `.L`, `.HK`, `.T`)."
    ]

    timeframe = cfg.get("investment_timeframe", "medium")
    if timeframe in _TIMEFRAME_CONTEXT:
        parts.append(_TIMEFRAME_CONTEXT[timeframe])

    focus = cfg.get("analysis_focus", "balanced")
    if focus in _FOCUS_CONTEXT:
        parts.append(_FOCUS_CONTEXT[focus])

    return " ".join(parts)

def create_msg_delete():
    def delete_messages(state):
        """Clear messages and add placeholder for Anthropic compatibility"""
        messages = state["messages"]

        # Remove all messages
        removal_operations = [RemoveMessage(id=m.id) for m in messages]

        # Add a minimal placeholder message
        placeholder = HumanMessage(content="Continue")

        return {"messages": removal_operations + [placeholder]}

    return delete_messages


        
