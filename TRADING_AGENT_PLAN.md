# Indian Market Trading Agent Architecture

## Goal
Build a complete automated trading system for the Indian market (NIFTY, BANKNIFTY, top Indian stocks) that provides buy/sell recommendations based on technical analysis.

## Current Constraints
The DSH harness doesn't provide direct access to stock market data through cordis_inspect tools. This solution will:

1. Document what Cordis services are available
2. Implement a technical analysis framework using available patterns
3. Create a recommendation engine with profit potential scoring
4. Manage user input for trade confirmation
5. Provide daily recommendations with execution workflow

## Analysis Framework (Available in DSH)

### Technical Indicators Available:
Based on typical DSH Cordis methods, expect to find access to:
- Moving Averages (SMA, EMA calculations)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume analysis
- Support/Resistance detection

### Market Analysis Phases:

**Phase 1: Index Analysis**
- NIFTY 50 trend identification
- BANKNIFTY parallel movements
- Trend strength assessment (BOS, EMA divergences)

**Phase 2: Stock Level Analysis**
Top stocks to analyze: Tata Steel, Reliance Industries, HDFC Bank, ICICI Bank, Infosys, L&T, BHEL, Adani Power

**Phase 3: Signal Generation**
- Entry criteria (RSI <30 oversold + MACD bullish, or RSI >70 overbought + pullback)
- Stop-loss levels (below recent swing low for BUY positions)
- Take-profit targets (above resistance for BUY, support for SELL)

**Phase 4: Profitability Scoring**
Score each potential trade on:
- Entry quality
- Risk/reward ratio (minimum 1:2 recommended)
- Market sentiment alignment
- Volume confirmation

## Execution Workflow

1. **Daily Data Collection**: Query available market endpoints via cordis_inspect
2. **Analysis Engine**: Run technical indicators and trend analysis
3. **Signal Generation**: Identify high-probability BUY/SELL signals
4. **Recommendation Assembly**: Score and rank candidates by profit potential
5. **User Confirmation**: Present recommendations to user for trade execution input
6. **Trade Execution**: Execute via DSH tool system with proper risk management

## Files to Create
- `TRADING_AGENT_PLAN.md` (this file) - Architecture documentation
- `DAYLY_MARKET_RECOMMENDATIONS/` directory for generated reports
- `TRADE_EXECUTION_LOGS/` directory for execution history

## Next Steps
1. Inspect available Cordis Service/Tool methods through cordis_inspect_list
2. Query specific methods to understand available schemas
3. Build recommendation engine based on schema documentation
4. Create daily analysis workflow
5. Implement user input confirmation mechanism
