# The Trade Floor

AI-powered multi-agent financial analysis. A team of specialized AI agents debates, researches, and produces a structured trade decision on any stock or ETF — covering market data, news, fundamentals, and social sentiment.

> **No coding required.** This guide uses Claude Code to handle all setup for you. Just copy and paste.

---

## What it does

You enter a ticker and a date. The system runs a full analyst pipeline:

1. **Analyst Team** — Market, News, Fundamentals, and Social Sentiment analysts pull live data and write independent reports
2. **Research Team** — A Bull and Bear researcher debate the stock. A Research Manager arbitrates and produces an investment thesis
3. **Trader** — Translates the thesis into a concrete trade plan
4. **Risk Management** — Aggressive, Conservative, and Neutral analysts stress-test the plan
5. **Portfolio Manager** — Issues the final BUY / SELL / HOLD decision with sizing guidance

Optional: **ETF Portfolio Mode** — if your ticker is an ETF (e.g. SPY, QQQ), it analyzes each top holding individually and produces position sizing and rebalancing recommendations.

---

## Prerequisites

You need two things installed before starting. Both are free to download.

### 1. Python 3.11 or newer

Download from: **https://www.python.org/downloads**

During installation, check the box that says **"Add Python to PATH"** before clicking Install. This is important.

### 2. Claude Desktop (with a Max plan)

Download from: **https://claude.ai/download**

Sign in with your Anthropic account. You need a **Claude Max plan** — this is what powers the analysis and handles the setup for you. No separate API key is needed.

---

## Setup (one-time, ~5 minutes)

Once you have Python and Claude Desktop installed:

**1. Open Claude Desktop**

**2. Copy the prompt below and paste it into Claude**

```
Please set up The Trade Floor on my computer. Do the following steps:

1. Check if git is installed. If not, tell me to install it from https://git-scm.com/download/win and wait.
2. Clone this repository to my Desktop: https://github.com/thewimpykid/tradingagents.git — save it in a folder called TradingAgents on my Desktop.
3. Check if uv is installed by running: uv --version
   If it is not installed, install it by running: powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
4. Navigate into the TradingAgents folder and run: uv sync
   This installs all dependencies. It may take 2-3 minutes.
5. Once complete, confirm setup is done and tell me to use the run prompt to start the app.
```

Claude will execute each step and tell you when it is done. If anything goes wrong, it will tell you exactly what to fix.

---

## Running the app

Every time you want to run the app, open Claude Desktop and paste this prompt:

```
Please start The Trade Floor. Navigate to the TradingAgents folder on my Desktop and run: uv run tradingagents
```

Claude will launch the app in a terminal window. You will then see a step-by-step wizard — no more coding needed from that point. Just use your keyboard to answer the questions.

---

## Using the wizard

Once the app launches, it walks you through a series of questions. Use **arrow keys** to navigate, **Enter** to confirm, and **Space** to select/deselect checkboxes.

| Step | What you choose |
|------|----------------|
| 1 | **Ticker symbol** — e.g. `AAPL`, `SPY`, `MSFT`, `CNC.TO`, `0700.HK` |
| 2 | **Analysis date** — the date to analyze (YYYY-MM-DD) |
| 3 | **Output language** — English, Chinese, Japanese, Spanish, and more |
| 4 | **Analyst team** — which analysts to include (select all for full coverage) |
| 5 | **Research depth** — Shallow (fast, ~3 min) / Medium (~8 min) / Deep (~20 min) |
| 6 | **AI provider** — select **Claude Code** |
| 7 | **AI models** — select the defaults unless you have a reason to change |
| 8 | **Thinking mode** — skip if using Claude Code (no extra config needed) |
| 9 | **Investment timeframe** — Short-term (days), Medium-term (weeks), Long-term (months+) |
| 10 | **Analysis focus** — Balanced / Fundamentals / Technical / Sentiment |
| 11 | **ETF Portfolio Mode** — if your ticker is an ETF, select Yes to analyze its top holdings |

After the analysis completes, you will be asked if you want to save and display the full report.

---

## Supported tickers

Any ticker supported by Yahoo Finance. Include the exchange suffix for non-US stocks:

| Suffix | Exchange |
|--------|----------|
| *(none)* | US markets (NYSE, NASDAQ) |
| `.TO` | Toronto Stock Exchange |
| `.L` | London Stock Exchange |
| `.T` | Tokyo Stock Exchange |
| `.HK` | Hong Kong Stock Exchange |
| `.AX` | Australian Securities Exchange |

---

## Saved reports

Reports are saved automatically under:
```
Desktop\TradingAgents\logs\<TICKER>\<DATE>\reports\
```

Each report contains:
```
1_analysts/        market.md, news.md, fundamentals.md, sentiment.md
2_research/        bull.md, bear.md, manager.md
3_trading/         trader.md
4_risk/            aggressive.md, conservative.md, neutral.md
5_portfolio/       decision.md
6_etf_portfolio/   portfolio_report.md   (ETF mode only)
complete_report.md
```

---

## Troubleshooting

If anything goes wrong, open Claude Desktop and describe the error. Example:

```
I am trying to run The Trade Floor and I got this error: [paste the error here]. Please fix it.
```

Claude will diagnose and fix it for you.

**Common issues:**

- **"Python not found"** — Reinstall Python and make sure to check "Add Python to PATH" during setup
- **"git is not recognized"** — Install git from https://git-scm.com/download/win, then restart Claude Desktop
- **"No holdings data"** — The ticker may not be an ETF, or Yahoo Finance does not have holdings data for it
- **Analysis is slow** — Normal. Deep research with all analysts can take 15-20 minutes. This is the AI doing thorough work.

---

## Disclaimer

For research and educational purposes only. Not financial advice. All analysis is AI-generated and may be inaccurate. Always do your own due diligence before making investment decisions.
