# Indian Market Trading Agent - Implementation Guide

## Quick Start Script (Demo Mode)

This script demonstrates the agent in demo mode using mock data:

```bash
python INDIAN_MARKET_TRADE_AGENT.py
```

### Demo Output Format:

```
======================================================================
🚀 INDIAN MARKET TRADING AGENT - INITIAL SETUP
======================================================================

Today's Date: 2026-11-11T06:00:00+05:30[Asia/Calcutta]

======================================================================
📊 DAILY MARKET ANALYSIS - TECHNICAL INDICATORS
======================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAILY MARKET OVERVIEW - INDIAN STOCKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NIFTY 50: ₹19500.00 (Current Price)
📈 Momentum: BULLISH

BANKNIFTY: ₹18450.00
(Parallel to NIFTY)

TREND INDICATORS:
- Moving averages showing: UPTREND
- Current trend: UP

KEY SIGNALS:
BUY OPPORTUNITIES:
1. Tata Steel @ Entry ₹23000 - Score: 85/100 | Profit: +₹500 | R: 1:3
   Reasoning: RSI in oversold zone + Uptrend alignment

SELL OPPORTUNITIES:
1. HDFC Bank @ Entry ₹1580 - Score: 45/100 | Risk: MEDIUM | Profit: X points

RECOMMENDATIONS SUMMARY:
- BUY positions to add: [3] lots
- SELL positions to remove: [2] lots
- Cash position: ₹1200000

EXECUTION INSTRUCTIONS:
User please confirm which positions to trade and execution method before executing.
```

## Understanding the System Components

### Files Created:

1. `INDIAN_MARKET_TRADE_AGENT.py` - Main implementation
   - MarketData class for tracking indices and stocks
   - TechnicalIndicators class for RSI, MACD calculations
   - RecommendationEngine for signal scoring
   - UserInterface for report generation

2. `MARKET_AGENT_INSTRUCTIONS.md` - Operational documentation
   - System architecture
   - Workflow process
   - Risk management rules
   - Troubleshooting guide

3. `DAYLY_MARKET_RECOMMENDATIONS.html` - Report template
   - HTML report with styling
   - Table-based display
   - Score visualization

## Technical Indicators Implemented

### 1. RSI (Relative Strength Index)
- Period: 14 days (standard)
- Overbought (>70): Sell signal if in downtrend
- Oversold (<30): Buy signal if in uptrend
- Divergence detection for reversal signals

### 2. MACD (Moving Average Convergence Divergence)
- Fast period: 12
- Slow period: 26
- Signal period: 9
- Detects momentum changes and trend direction

### 3. Moving Averages
- SMA (Simple Moving Average): For trend identification
- EMA (Exponential Moving Average): For momentum tracking
- Crossover detection for signal generation

### 4. Support/Resistance Detection
- Simple swing point identification
- Price position relative to recent lows/highs
- Trend-following support/resistance zones

## Signal Scoring Formula

Profit Potential Score = (RSI Position × 30%) + (Trend Alignment × 40%) + (Volume Confirmation × 10%)

```python
def calculate_profit_score(entry_price, exit_price, rsi, trend):
    # Calculate potential profit percentage
    # Apply RSI bonus based on trend alignment
    # Add volume confirmation weight
    # Return score and reasoning string
```

## User Input Workflow

The system prompts user for each position with clear actions:

**Buy Positions:**
```
Are you sure you want to trade this position? (y/n)

[Response options] y / n / skip
```

**Sell/Remove Positions:**
```
Are you sure you want to take this position? (y/n)

[Response options] y / n / skip
```

## Risk Management Implemented

1. **Maximum Position Size**: 30% of portfolio per day
2. **Stop-Loss**: 5% below entry price (minimum 2 lots)
3. **Take-Profit Targets**: +8%, then +15% above first target
4. **Cash Buffer**: 20% minimum for liquidity
5. **Max Loss Protection**: Stop trading after 2 consecutive losers

## Next Steps for Production Implementation

### Required Integration:
1. NSE/BSE API connection
2. Historical data storage
3. User authentication system
4. Execution engine
5. Portfolio management module

### Recommended Tools:
- Python financial libraries: `pandas`, `numpy`
- WebSocket for real-time data streams
- RESTful API clients for market data

## Sample Input Data Structure

### MarketData Class (mock):
```python
class MarketData:
    def __init__(self):
        self.index_data = {
            'NIFTY': {'current_price': 19500, 'timestamp': '2026-11-11T', 'trend': 'UP'},
            'BANKNIFTY': {'current_price': 18450, 'timestamp': '2026-11-11T', 'trend': 'UP'}
        }
    
    def update(self, price: float, direction: str = 'NEUTRAL'):
        self.index_data['NIFTY'] = {
            'current_price': price,
            'timestamp': date.today().isoformat(),
            'trend': direction
        }
```

### Stock Analysis (mock):
```python
stock_entry = {
    'name': 'Tata Steel',
    'sector': 'Steel/Infrastructure',
    'entry_price': 23000,
    'exit_price': 23500,  # Would fetch from API
    'rsi': 28,           # Oversold = good buy signal
    'macd': 0.12,       # Bullish crossover
    'trend': 'UP',
    'support': 22900,
    'resistance': 23700
}
```

## Testing the System

### Manual Testing Steps:
1. Run `python INDIAN_MARKET_TRADE_AGENT.py`
2. Review output for correct format
3. Verify data structures and calculations
4. Test with modified stock data to check scoring logic
5. Check HTML report renders correctly

### API Integration Testing:
To test against real market data:
1. Replace mock values with actual API calls
2. Connect to NSE/BSE WebSocket feeds
3. Test indicator calculations with live price history
4. Verify signal generation accuracy

## Documentation References

- `MARKET_AGENT_INSTRUCTIONS.md` - Full operational guide
- `DAYLY_MARKET_RECOMMENDATIONS.html` - User report template
- `INDIAN_MARKET_TRADE_AGENT.py` - Main implementation code

## Support and Contact

For questions or issues:
1. Review all documentation files above
2. Check the Python script for error messages
3. Verify system permissions in DSH environment
4. Ensure correct workspace path is used when running

---

**System Version**: 1.0.0  
**Last Updated**: 2026-11-11  
**Status**: Ready for Demo Testing
