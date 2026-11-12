# Indian Market Trading Agent

A Python project exploring rule-based market analysis and trade-recommendation workflows for Indian equities and market indices.

> **Project status: experimental / under active development.**
> This repository is not a broker-connected trading platform and must not be treated as a source of investment advice. Market-data endpoints, indicator calculations, scoring logic and sample outputs require independent validation before any real-money use.

## Overview

The codebase contains prototype components for:

- Market and stock data structures for NIFTY and BANKNIFTY.
- Technical-analysis experiments involving RSI, MACD, moving averages and trend heuristics.
- Rule-based recommendation and scoring experiments.
- Demo output and comparison scripts.
- Text and Markdown implementation notes, plus an HTML report.

Some scripts use simulated values or placeholder API details. The presence of a market-data integration script does **not** imply that a supported, authenticated or reliable live feed is configured.

## Repository contents

| File | Purpose |
| --- | --- |
| `INDIAN_MARKET_TRADE_AGENT.py` | Main prototype: market data structures, indicator experiments and recommendation workflow |
| `DAILY_MARKET_ANALYSIS.py` | Daily analysis/reporting prototype; includes external market-data request code |
| `MARKET_API_INTEGRATION.py` | Experimental market-data integration module |
| `DEMO_AND_PRODUCTION_COMPARISON.py` | Demo/production comparison output |
| `GENERATE_DEMO_RESULTS.py` | Demo-result generation |
| `PRESSING_RUN.py` | Additional experimental market-analysis script |
| `DAYLY_MARKET_RECOMMENDATIONS.html` | HTML report example/template |
| `README_TRADING_AGENT.md` | Additional project overview |
| `IMPLEMENTATION_GUIDE.md` | Implementation notes |
| `MARKET_ANALYSIS_ENGINE.md` | Analysis-engine notes |
| `MARKET_AGENT_INSTRUCTIONS.md` | Agent workflow notes |
| `TRADING_AGENT_PLAN.md`, `TRADING_AGENT_SUMMARY.md` | Planning and summary documents |

The repository also contains demo outputs and progress notes. These are retained as project artefacts; they should not be interpreted as independent verification of trading performance.

## Getting started

### Requirements

- Python 3.10 or newer
- pip

### Setup

Clone the repository:

```bash
git clone https://github.com/Deepak-kumar10/dsh-market-trading-agent.git
cd dsh-market-trading-agent
```

Create and activate a virtual environment.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the declared dependency:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the prototypes

The main prototype can be started with:

```bash
python INDIAN_MARKET_TRADE_AGENT.py
```

The daily analysis script can be started with:

```bash
python DAILY_MARKET_ANALYSIS.py
```

Review the script and its data-source assumptions before running it. Some modules make external HTTP requests; availability, response formats and access policies of third-party endpoints can change. A successful script launch is not proof that the returned prices are current or correct.

## Technical-analysis concepts

The project explores common indicators and heuristics:

| Concept | Intended use |
| --- | --- |
| RSI | Momentum and overbought/oversold context |
| MACD | Momentum and trend confirmation |
| Moving averages | Trend smoothing and comparison |
| Support / resistance | Reference levels derived from historical prices |
| Rule-based scoring | Experimental ranking of candidate opportunities |

These are research components, not validated predictive models. Scores are not probabilities of profit, and example prices or recommendations may be simulated.

## Configuration and secrets

- Never commit API keys, access tokens, broker credentials, passwords or personal data.
- Keep local secrets in environment variables or an untracked `.env` file.
- Do not put credentials directly in source code or GitHub Actions YAML.
- Rotate any credential that has ever been committed to a public repository; deleting it in a later commit does not invalidate the exposure.
- Confirm the terms and permitted use of any market-data provider before integrating it.

## Development checks

Run Python's syntax compiler against the project scripts:

```bash
python -m compileall -q .
```

Install dependencies from `requirements.txt` in a virtual environment. Automated checks are configured in GitHub Actions and run on pushes and pull requests.

## Roadmap

- [ ] Audit and correct indicator formulas with reference datasets and unit tests.
- [ ] Separate mock data, historical data and live data providers.
- [ ] Replace placeholder endpoints with a documented, permitted market-data provider.
- [ ] Add data validation, timestamps, exchange-calendar handling and stale-data detection.
- [ ] Add reproducible backtesting with transaction costs and slippage.
- [ ] Define risk controls and position sizing independently of recommendation scores.
- [ ] Add structured logging and configuration management.
- [ ] Review all scripts and documentation for accuracy before describing features as production-ready.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. Include reproducible steps, sample inputs and expected results for bug reports.

## Disclaimer

This repository is provided for educational and research purposes only. It is not financial, investment, tax or legal advice, and it does not recommend any particular security or transaction. Trading and investing involve risk, including loss of capital. Past or simulated results do not guarantee future outcomes.

Do not connect this prototype to a live brokerage account or use it to place real orders without a full independent code, data, security, compliance and risk review.

## Maintainer

**Deepak Kumar** — [GitHub profile](https://github.com/Deepak-kumar10)

---

If you find a problem or have a suggestion, please open a GitHub Issue.
