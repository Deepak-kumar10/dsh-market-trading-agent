# 📈 Indian Market Trading Agent System

## Overview

A comprehensive automated trading system designed for the Indian stock market (NSE/NIFTY, BANKNIFTY and top 20 Indian stocks). The agent analyzes technical indicators, trend patterns, and provides high-probability buy/sell recommendations with profit potential scoring.

## 🎯 Capabilities

- ✅ **Market Analysis**: NIFTY 50 & BANKNIFTY trend tracking
- ✅ **Technical Indicators**: RSI, MACD, Moving Averages, Bollinger Bands
- ✅ **Pattern Recognition**: Support/Resistance, trend identification
- ✅ **Profit Scoring**: Quantified buy/sell recommendations (0-100 scale)
- ✅ **Risk Management**: 30% max position, 5% stop-loss, automated limits
- ✅ **User Interface**: Interactive confirmation workflow

## 📁 Project Structure

```
default-workspace/
├── INDIAN_MARKET_TRADE_AGENT.py    # Main implementation
├── MARKET_AGENT_INSTRUCTIONS.md     # Operational guide (650+ lines)
├── DAYLY_MARKET_RECOMMENDATIONS.html # Report template
├── IMPLEMENTATION_GUIDE.md           # Development guide
└── TRADING_AGENT_SUMMARY.md         # System summary

# Files to create in production:
# ├── MARKET_ANALYSIS/
# │   └── 2026_11_11.txt          # Daily analysis report
# ├── TRADE_EXECUTION_LOGS/
# │   └── {date}/                 # Execution history
```

## 🚀 Quick Start

### Demo Mode:
```bash
cd default-workspace
python INDIAN_MARKET_TRADE_AGENT.py
```

### Expected Output Format:
```
======================================================================
📊 DAILY MARKET ANALYSIS - TECHNICAL INDICATORS
======================================================================

NIFTY 50: ₹19500.00 (Current Price)
BANKNIFTY: ₹18450.00
TREND INDICATORS: UPTREND

BUY OPPORTUNITIES:
1. Tata Steel @ Entry ₹23000 - Score: 85/100 | Profit: +₹500
   Reasoning: RSI in oversold zone + Uptrend alignment

EXECUTION INSTRUCTIONS:
User please confirm which positions to trade and execution method before executing.
```

## 📊 Report Template (HTML)

Visit `DAYLY_MARKET_RECOMMENDATIONS.html` for:
- Formatted market overview
- Individual stock analysis tables
- Profit scoring visualization
- Execution workflow instructions

## 🔧 System Architecture

### Component 1: MarketData Class
Handles index and stock data tracking

```python
class MarketData:
    - update(nifty_price: float, trend: str)
    - set_stock(name: str, price: float, rsi: int)
    - index_data: dict with current market state
```

### Component 2: TechnicalIndicators Class
Calculates technical analysis signals

```python
- calculate_rsi(prices: List[float]) -> int
- calculate_macd(prices: List[float], fast=12, slow=26) -> dict
- detect_trend_direction(prices: List[float], ma_period=50) -> UP/DOWN/NEUTRAL
```

### Component 3: RecommendationEngine Class
Generates and scores trading signals

```python
def generate_recommendations(market_data: MarketData, stock_price: float) -> Dict
    # Returns: buys[], sells[], neutral[] with scoring
```

## 📈 Technical Analysis Framework

### Indicators Applied to All Stocks:
1. **RSI (14-period)** - Overbought (>70), Oversold (<30)
2. **MACD** - Momentum signals and trend direction
3. **EMA(50,90)** - Trend confirmation zones
4. **Support/Resistance** - Swing-based level detection

### Scoring Criteria:
- RSI Position Alignment (30%)
- Trend Direction Confirmation (40%)
- Volume Spike Confirmation (10%)
- Time Horizon Fit (20%)

## ⚙️ Risk Management Defaults

| Parameter | Value |
|-----------|-------|
| Max Position Size | 30% portfolio daily |
| Stop-Loss | 5% below entry |
| Take-Profit 1 | +8% above entry |
| Take-Profit 2 | +15% above target |
| Min Cash Reserve | 20% portfolio |
| Max Losing Trades Before Pause | 2 |

## 🔍 User Input Workflow

Each trade position is confirmed before execution:

**Buy Confirmation:**
```
Are you sure you want to trade this position? (y/n) [y/n]
```

**Sell Confirmation:**
```
Are you sure you want to take this position? (y/n) [y/n]
```

## 📋 Supported Stocks (Top 20 Indian)

| Stock | Sector | Entry Price Range |
|-------|--------|-------------------|
| Tata Steel | Infrastructure | ₹20,000 - ₹25,000 |
| Reliance Industries | Oil & Consumables | ₹50,000 - ₹60,000 |
| HDFC Bank | Banking | ₹1,380 - ₹1,590 |
| ICICI Bank | Banking | ₹870 - ₹990 |
| Infosys | IT | ₹11,000 - ₹13,000 |

## 🐛 Common Issues & Solutions

### Issue: "No price data"
**Solution**: Use mock values for development (script includes sample prices)

### Issue: Slow Performance
**Solution**: Optimize indicator calculations; batch API calls in production

### Issue: Conflicting Signals
**Solution**: Apply weighted scoring based on trend alignment focus

## 📊 Daily Workflow

```
06:00  - Data collection (NIFTY/BANKNIFTY prices)
08:00  - Technical analysis (RSI, MACD, trends)
10:00  - Signal generation with scoring
11:30  - Report presentation to user
12:00  - User confirmation workflow
```

## 🔮 Future Enhancements

- [ ] NSE/BSE WebSocket integration
- [ ] Historical data API access
- [ ] Portfolio management module
- [ ] Mobile dashboard interface
- [ ] AI-powered signal refinement
- [ ] Backtesting framework
- [ ] Alert systems for critical levels

## 📞 Support Resources

- **Documentation**: `MARKET_AGENT_INSTRUCTIONS.md`
- **Implementation Guide**: `IMPLEMENTATION_GUIDE.md`
- **Agent Code**: `INDIAN_MARKET_TRADE_AGENT.py`

## ⚖️ Legal & Compliance

⚠️ DISCLAIMER: This trading system is for educational purposes only. Trading involves risk and may not be suitable for all investors. Past performance does not guarantee future results. Always conduct your own research before making investment decisions.

---

**System Version**: 1.0  
**Last Updated**: 2026-11-11  
**Status**: Development - Phase 1 Complete  
**Author**: Automated Agent System
