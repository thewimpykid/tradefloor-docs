# The Trade Floor

AI-powered multi-agent financial analysis. A team of specialized AI agents debates, researches, and produces a structured trade decision on any stock or ETF — covering market data, news, fundamentals, and social sentiment.

> **No coding required.** This guide uses Claude to handle all setup for you. Just copy and paste the prompts below.

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

Two things to install before starting. Both are free.

### 1. Python 3.11 or newer

Download from: **https://www.python.org/downloads**

> During installation, check the box that says **"Add Python to PATH"** before clicking Install.

### 2. Claude Desktop (Max plan)

Download from: **https://claude.ai/download**

Sign in with your Anthropic account. A **Max plan** subscription is required — this is what runs the analysis and handles the setup for you. No separate API key needed.

---

## Setup (one-time, ~5 minutes)

Once Python and Claude Desktop are installed:

**Open Claude Desktop, copy the prompt below, and paste it in.**

```
Please set up The Trade Floor on my computer. Do the following:

1. Check if git is installed by running: git --version
   If it is not installed, tell me to download it from https://git-scm.com/download/win, install it, then come back.

2. Clone this repository to my Desktop into a folder called TradeFloor:
   git clone https://github.com/thewimpykid/tradefloor-docs.git "C:\Users\%USERNAME%\Desktop\TradeFloor"

3. Check if uv is installed by running: uv --version
   If it is not found, install it by running:
   powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
   Then close and reopen this Claude window so the new PATH takes effect, and continue.

4. Navigate into the TradeFloor folder and run: uv sync
   This installs all dependencies. It may take 2-3 minutes the first time.

5. Once complete, tell me setup is finished and show me the run prompt.
```

Claude will run each step and tell you when it is done. If anything goes wrong, it will tell you what to fix.

---

## Running the app

Every time you want to run the app, open Claude Desktop and paste this:

```
Please start The Trade Floor. Run the following command:
uv run tradingagents --app-dir "C:\Users\%USERNAME%\Desktop\TradeFloor"
```

> **Simpler alternative:** Open a terminal in the TradeFloor folder (right-click the folder → Open in Terminal) and run: `uv run tradingagents`

The app launches a wizard. No more commands after that — just use your keyboard to answer the questions.

---

## Using the wizard

Arrow keys to navigate, Enter to confirm, Space to select/deselect.

| Step | What you choose |
|------|----------------|
| 1 | **Ticker symbol** — e.g. `AAPL`, `SPY`, `MSFT`, `CNC.TO`, `0700.HK` |
| 2 | **Analysis date** — format: YYYY-MM-DD (e.g. 2026-05-01) |
| 3 | **Output language** — English, Chinese, Japanese, Spanish, and more |
| 4 | **Analyst team** — select all for full coverage |
| 5 | **Research depth** — Shallow (~3 min) / Medium (~8 min) / Deep (~20 min) |
| 6 | **AI provider** — select **Claude Code** |
| 7 | **AI models** — leave as defaults |
| 8 | **Thinking mode** — skip (not needed for Claude Code) |
| 9 | **Investment timeframe** — Short-term (days), Medium-term (weeks), Long-term (months+) |
| 10 | **Analysis focus** — Balanced / Fundamentals / Technical / Sentiment |
| 11 | **ETF Portfolio Mode** — select Yes if your ticker is an ETF |

After the analysis finishes, you will be asked if you want to save and display the full report.

---

## Supported tickers

Any ticker on Yahoo Finance. Add an exchange suffix for non-US stocks:

| Suffix | Exchange |
|--------|----------|
| *(none)* | US markets — NYSE, NASDAQ |
| `.TO` | Toronto Stock Exchange |
| `.L` | London Stock Exchange |
| `.T` | Tokyo Stock Exchange |
| `.HK` | Hong Kong Stock Exchange |
| `.AX` | Australian Securities Exchange |

---

## Where reports are saved

```
Desktop\TradeFloor\logs\<TICKER>\<DATE>\reports\
  1_analysts\        market.md, news.md, fundamentals.md, sentiment.md
  2_research\        bull.md, bear.md, manager.md
  3_trading\         trader.md
  4_risk\            aggressive.md, conservative.md, neutral.md
  5_portfolio\       decision.md
  6_etf_portfolio\   portfolio_report.md     (ETF mode only)
  complete_report.md
```

---

## Troubleshooting

Paste this into Claude Desktop with your error:

```
I am trying to run The Trade Floor and I got this error: [paste error here]. Please fix it.
```

**Common issues:**

| Problem | Fix |
|---------|-----|
| "Python not found" | Reinstall Python, check "Add Python to PATH" during install |
| "git is not recognized" | Install git from https://git-scm.com/download/win, restart Claude |
| "uv not found" | Close and reopen Claude Desktop after installing uv |
| "No holdings data" | Ticker is not an ETF, or Yahoo Finance has no holdings data for it |
| Analysis very slow | Normal — Deep mode with all analysts takes 15-20 min |

---

## Disclaimer

For research and educational purposes only. Not financial advice. All output is AI-generated and may be inaccurate. Do your own due diligence before making any investment decisions.
