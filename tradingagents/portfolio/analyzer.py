"""Quick per-holding analysis and portfolio-level synthesis for ETFs."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple


_HOLDING_PROMPT_TMPL = """You are a portfolio analyst reviewing a single equity holding inside an ETF.

ETF: {etf_ticker}
Holding: {name} ({symbol})
ETF weight: {weight:.2f}%
Analysis date: {analysis_date}

In 3-5 sentences give a quick assessment of this holding's current investment merit.
Then respond with ONLY a JSON object (no prose before or after):

{{
  "symbol": "{symbol}",
  "sentiment": "Bullish" | "Neutral" | "Bearish",
  "conviction": "High" | "Medium" | "Low",
  "key_risk": "<one sentence>",
  "key_catalyst": "<one sentence>",
  "suggested_action": "Overweight" | "Maintain" | "Underweight",
  "rationale": "<2-3 sentence summary>"
}}
"""

_SYNTHESIS_PROMPT_TMPL = """You are a senior portfolio manager reviewing an ETF.

ETF: {etf_ticker}
Analysis date: {analysis_date}
Top {n} holdings already analysed (JSON array):
{holdings_json}

Provide a portfolio-level synthesis covering:
1. Overall portfolio outlook (Bullish / Neutral / Bearish) with 2-sentence rationale
2. Top 3 highest-conviction overweight ideas (symbol + one-line reason)
3. Top 3 underweight / trim candidates (symbol + one-line reason)
4. Key concentration risks (sector, single-name, factor)
5. Suggested rebalancing action in 2-3 sentences

Respond ONLY with this JSON (no prose outside):
{{
  "etf": "{etf_ticker}",
  "outlook": "Bullish" | "Neutral" | "Bearish",
  "outlook_rationale": "<2 sentences>",
  "overweight": [{{"symbol": "...", "reason": "..."}}],
  "underweight": [{{"symbol": "...", "reason": "..."}}],
  "concentration_risks": "<2 sentences>",
  "rebalancing_action": "<2-3 sentences>"
}}
"""


def _call_llm(prompt: str, config: Dict[str, Any]) -> str:
    """Single LLM call returning the raw text response."""
    from tradingagents.llm_clients.factory import create_llm_client
    from langchain_core.messages import HumanMessage

    provider = config.get("llm_provider", "openai")
    model = config.get("quick_think_llm", "gpt-4o-mini")
    base_url = config.get("backend_url")

    client = create_llm_client(provider, model, base_url)
    llm = client.get_llm()
    result = llm.invoke([HumanMessage(content=prompt)])
    return str(result.content)


def _safe_parse_json(text: str) -> Optional[dict]:
    """Extract and parse the first JSON object from text."""
    import re
    # Fenced block first
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    # Greedy first-{ to last-}
    m = re.search(r"(\{.*\})", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return None


def analyze_holding(
    symbol: str,
    name: str,
    weight: float,
    etf_ticker: str,
    analysis_date: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Run a single quick LLM call for one ETF holding.

    Returns a dict with keys: symbol, sentiment, conviction, key_risk,
    key_catalyst, suggested_action, rationale.
    Falls back to a placeholder on any error.
    """
    prompt = _HOLDING_PROMPT_TMPL.format(
        etf_ticker=etf_ticker,
        name=name,
        symbol=symbol,
        weight=weight,
        analysis_date=analysis_date,
    )
    try:
        raw = _call_llm(prompt, config)
        parsed = _safe_parse_json(raw)
        if parsed and "sentiment" in parsed:
            parsed.setdefault("symbol", symbol)
            parsed["weight"] = weight
            parsed["name"] = name
            return parsed
    except Exception as e:
        pass

    return {
        "symbol": symbol,
        "name": name,
        "weight": weight,
        "sentiment": "Neutral",
        "conviction": "Low",
        "key_risk": "Analysis unavailable",
        "key_catalyst": "Analysis unavailable",
        "suggested_action": "Maintain",
        "rationale": f"Could not complete analysis for {symbol}.",
    }


def synthesize_portfolio(
    etf_ticker: str,
    holding_results: List[Dict[str, Any]],
    analysis_date: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Run a synthesis LLM call across all analysed holdings."""
    prompt = _SYNTHESIS_PROMPT_TMPL.format(
        etf_ticker=etf_ticker,
        analysis_date=analysis_date,
        n=len(holding_results),
        holdings_json=json.dumps(holding_results, indent=2),
    )
    try:
        raw = _call_llm(prompt, config)
        parsed = _safe_parse_json(raw)
        if parsed and "outlook" in parsed:
            return parsed
    except Exception:
        pass

    return {
        "etf": etf_ticker,
        "outlook": "Neutral",
        "outlook_rationale": "Synthesis unavailable.",
        "overweight": [],
        "underweight": [],
        "concentration_risks": "Analysis unavailable.",
        "rebalancing_action": "No recommendation available.",
    }


def run_portfolio_analysis(
    etf_ticker: str,
    top_n: int,
    analysis_date: str,
    config: Dict[str, Any],
    progress_callback=None,
) -> Dict[str, Any]:
    """Full ETF portfolio analysis: per-holding + synthesis.

    progress_callback(i, total, symbol) called after each holding completes.
    Returns dict with keys: etf, holdings, synthesis.
    """
    from .holdings import get_etf_holdings

    holdings = get_etf_holdings(etf_ticker, top_n)
    if not holdings:
        return {
            "etf": etf_ticker,
            "holdings": [],
            "synthesis": {
                "etf": etf_ticker,
                "outlook": "Neutral",
                "outlook_rationale": f"No holdings data found for {etf_ticker}. It may not be an ETF or data is unavailable.",
                "overweight": [],
                "underweight": [],
                "concentration_risks": "N/A",
                "rebalancing_action": "N/A",
            },
            "error": f"No holdings data for {etf_ticker}.",
        }

    holding_results: List[Dict[str, Any]] = []
    total = len(holdings)
    for i, (sym, weight, name) in enumerate(holdings):
        result = analyze_holding(sym, name, weight, etf_ticker, analysis_date, config)
        holding_results.append(result)
        if progress_callback:
            progress_callback(i + 1, total, sym)

    synthesis = synthesize_portfolio(etf_ticker, holding_results, analysis_date, config)

    return {
        "etf": etf_ticker,
        "holdings": holding_results,
        "synthesis": synthesis,
    }
