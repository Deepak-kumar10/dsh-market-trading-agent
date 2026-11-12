# Market Analysis Engine - Technical Indicators & Recommendations

## Available Methods for Data Access (Documented)

Based on cordis_inspect_list output, here are the available methods:

### Host Services
- **listService**: Get compact Service directory with service contracts
- **listEvents**: Get listener directory with event contracts
- **listConfigs**: Get plugin Config schema status and definitions
- **listTools**: Get all tools callable by Agent

### Client Services
- **listService**: Same as Host (Client-side capability)
- **listEvents**: Same as Host
- **Builtin**: Plain-JavaScript symbols for dynamic Client access

## Trading Analysis Framework

### Index-Level Analysis

**NIFTY 50 Index:**
- Current level tracking via price data queries
- Trend direction: Uptrend/Downtrend/Consolidation
- Momentum indicators (MACD, RSI)
- EMA alignments (20/60-day moving averages)
- Support/Resistance identification

**BANKNIFTY:**
- Often mirrors NIFTY movements with lag
- Volume analysis for confirmation signals
- Volatility assessment during trend phases

### Stock-Level Technical Analysis Framework

For key Indian stocks (Top 20), will apply:
1. Moving Averages:
   - SMA(20) for short-term trend
   - SMA(50) for medium-term trend  
   - EMA(90) for momentum direction
   - Golden/Death cross detection

2. RSI (Relative Strength Index):
   - Overbought: >70 (potential sell signal if declining)
   - Oversold: <30 (potential buy signal if increasing)
   - Position in current trend using Divergence detection

3. MACD (Moving Average Convergence Divergence):
   - Signal line crossing
   - Histogram momentum
   - Zero-line crossovers

4. Bollinger Bands:
   - Band compression/expansion
   - Price position relative to bands
   - Volatility measurement

5. Volume Analysis:
   - Volume spike confirmation
   - Relative volume metrics
   - Distribution patterns (accumulation/distribution)

## Trading Signal Generation Logic

### BUY Signals (Multi-Condition Priority)

1. **RSI Divergence**: RSI makes higher high but price makes lower high
2. **RSI Oversold Recovery**: RSI <30 turning up with upward momentum
3. **EMA Support Confirmation**: Price bounces from rising EMA lines
4. **MACD Bullish Cross**: MACD line crosses above signal line with bullish histogram
5. **Volume Spike**: Trading volume exceeds 20% average for entry

### SELL Signals (Multi-Condition Priority)

1. **RSI Overbought Recovery**: RSI >70 turning down with downward momentum
2. **EMA Resistance Breakdown**: Price falls below falling EMA lines
3. **MACD Bearish Cross**: MACD line crosses below signal line
4. **Volume Decline**: Trading volume drops below 15% average for exit confirmation
5. **Resistance Testing**: Price approaches/breaks key resistance levels

### Profit Potential Scoring Formula

For each potential BUY opportunity:

```
Profit Score = (EntryQuality × 30%) + (RiskReward Ratio × 40%) + (TrendAlignment × 20%) + (VolumeConfirmation × 10%) + (TimeHorizonFit × 5%)

Entry Quality (0-100):
- RSI position relative to current trend zone
- EMA alignment with price action
- Moving average convergence strength
- Volume confirmation intensity

RiskReward Ratio (0-200 points):
- Distance to nearest support for entry (minimum: 2:1)
- Average stop-loss level (minimum distance 5%)
- Target placement above resistance level

TrendAlignment (0-100 points):
- RSI alignment with current trend direction
- EMA slope agreement with price momentum
- Moving average convergence strength

VolumeConfirmation (0-50 points):
- Relative volume vs. historical average
- Volume spike at entry
- Consistent volume flow
```

## Daily Trading Workflow

### Morning Analysis Steps

1. **Index Check**: Query NIFTY BANKNIFTY current price and trend status
2. **Technical Scan**: Apply indicators to top 20 stocks
3. **Signal Filtering**: Remove signals below confidence threshold (40%)
4. **Profit Scoring**: Score remaining candidates by profit potential
5. **Final Recommendations**: Rank by score, select top 3-5 BUY and up to 5 SELL opportunities

### User Input Workflow

1. Display daily recommendations in clear format:
   - Asset | Action | Entry Price | Target Price | Risk (Points) | Recommendation Score
2. Ask user confirmation questions for each position
3. Receive explicit instruction before execution (not auto-trade)
4. Execute only when user confirms with "EXECUTE"

## Output Format Recommendations

### Daily Report Template
```
=============================================
DAILY MARKET ANALYSIS REPORT - INDIAN STOCKS
=============================================

NIFTY 50: ₹{level} {direction}{momentum_note}
BANKNIFTY: ₹{level} (parallel: {yes/no})

TREND INDICATORS:
- Moving averages showing: {alignment}
- Current trend: {uptrend|downtrend|consolidation}

KEY SIGNALS:
BUY OPPORTUNITIES:
1. [Stock] @ Entry ₹{price} - Score: X/100 | Profit: +₹{amount} | R: 1:2.5
   Reasoning: {multi_line_reasoning}

SELL OPPORTUNITIES:
1. [Stock] @ Entry ₹{price} - Score: X/100 | Profit: X points | R: 1:2
   Reasoning: {multi_line_reasoning}

RECOMMENDATIONS SUMMARY:
- BUY positions to add: {[count]} lots
- SELL positions to reduce: {[count]} lots
- Cash position: ₹[balance]

EXECUTION INSTRUCTIONS:
User please confirm which positions to trade and execution method before executing.
```

## Key Considerations for Indian Market

1. **High Volatility**: Use larger stop-loss levels (5% minimum)
2. **Sector Correlation**: Watch sector rotation, especially in banking/infrastructure
3. **Fundamental Support**: Price action may lag fundamentals; monitor quarterly reports
4. **News Impact**: Be cautious during news events; use volume filters to confirm interest
5. **Timeframes**: Daily/weekly patterns more reliable than intraday

## Risk Management

1. **Position Sizing**: Max 30% per trade, 15% total portfolio exposure
2. **Stop-Losses**: Fixed percentage (5%) for both BUY and SELL positions
3. **Take-Profits**: 
   - First target: 5-8% above entry
   - Second target: 10-15% above first target
4. **Max Loss Limiting**: 2 consecutive losing trades → pause new entries

---

**Note**: This analysis framework provides the logic structure. Actual implementation will require:
- External financial API integration (NSE/BSE)
- Data storage for historical indicators  
- User interface for displaying signals and confirming executions
- Execution via available DSH tool system

For now, this documentation serves as the design blueprint for building a functional trading agent within the harness's technical capabilities.
