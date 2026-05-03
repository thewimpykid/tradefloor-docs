"""Fetch ETF top holdings via yfinance."""
from __future__ import annotations

from typing import List, Tuple


def get_etf_holdings(ticker: str, top_n: int = 10) -> List[Tuple[str, float, str]]:
    """Return list of (symbol, weight_pct, holding_name) for the top N ETF holdings.

    Returns empty list if the ticker is not an ETF or data is unavailable.
    """
    try:
        import yfinance as yf
        etf = yf.Ticker(ticker)
        df = etf.funds_data.top_holdings
        if df is None or df.empty:
            return []
        # yfinance returns a DataFrame with columns: holdingName, holdingPercent
        # Index is the ticker symbol
        results: List[Tuple[str, float, str]] = []
        for sym, row in df.head(top_n).iterrows():
            weight = float(row.get("holdingPercent", 0.0)) * 100
            name = str(row.get("holdingName", sym))
            results.append((str(sym), weight, name))
        return results
    except Exception:
        return []
