"""
Indian Market Trading Agent - Technical Analysis & Recommendation System

This system provides automated analysis of Indian market data (NIFTY, BANKNIFTY)
and top Indian stocks with technical indicators and profit potential scoring.
"""

import json
import csv
from datetime import date
from typing import Dict, List, Optional, Tuple

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class MarketData:
    """Tracks market data for NIFTY 50, BANKNIFTY and top Indian stocks"""
    
    def __init__(self):
        self.index_data = {
            'NIFTY': {'current_price': None, 'timestamp': None, 'trend': None},
            'BANKNIFTY': {'current_price': None, 'timestamp': None, 'trend': None},
        }
        
        # Top 20 Indian stocks with placeholder data structure
        self.top_stocks = [
            {
                'name': 'Tata Steel', 'sector': 'Steel/Infrastructure',
                'current_price': None, 'rsi': None, 'macd': None, 'trend': None,
                'support': None, 'resistance': None,
                'score': 0, 'status': 'pending'  # Awaiting analysis
            },
            {
                'name': 'Reliance Industries', 'sector': 'Oil/Consumables',
                'current_price': None, 'rsi': None, 'macd': None, 'trend': None,
                'support': None, 'resistance': None,
                'score': 0, 'status': 'pending'
            },
            {
                'name': 'HDFC Bank', 'sector': 'Banking',
                'current_price': None, 'rsi': None, 'macd': None, 'trend': None,
                'support': None, 'resistance': None,
                'score': 0, 'status': 'pending'
            },
            {
                'name': 'ICICI Bank', 'sector': 'Banking',
                'current_price': None, 'rsi': None, 'macd': None, 'trend': None,
                'support': None, 'resistance': None,
                'score': 0, 'status': 'pending'
            },
            {
                'name': 'Infosys', 'sector': 'Information Technology',
                'current_price': None, 'rsi': None, 'macd': None, 'trend': None,
                'support': None, 'resistance': None,
                'score': 0, 'status': 'pending'
            },
        ]
    
    def update(self, current_level: float, trend_direction: str = "NEUTRAL"):
        """Update index data with new price movement"""
        self.index_data['NIFTY'] = {
            'current_price': current_level,
            'timestamp': date.today().isoformat(),
            'trend': trend_direction
        }
        
        # Update BANKNIFTY (typically mirrors NIFTY)
        self.index_data['BANKNIFTY'] = {
            'current_price': round(current_level * 1.023, 2),  # Approx 2.3% lag
            'timestamp': date.today().isoformat(),
            'trend': trend_direction
        }
    
    def set_stock(self, name: str, price: float, rsi: int = None, 
                   macd: float = None, trend: str = "UP", 
                   support: Optional[float] = None, resistance: Optional[float] = None):
        """Update stock analysis data"""
        self.top_stocks[-1]['current_price'] = price
        self.top_stocks[-1]['rsi'] = rsi
        self.top_stocks[-1]['macd'] = macd
        self.top_stocks[-1]['trend'] = trend
        
        # Simple support/resistance detection based on recent movement
        if trend == "UP" and resistance:
            self.top_stocks[-1]['support'] = round(resistance, 2)
        elif trend == "DOWN" and support:
            self.top_stocks[-1]['resistance'] = round(support, 2)

# ============================================================================
# TECHNICAL INDICATORS ANALYSIS
# ============================================================================

class TechnicalIndicators:
    """Analyzes technical indicators for market positions"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period=14):
        """Calculate RSI relative strength indicator"""
        if len(prices) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(len(prices) - 1):
            diff = prices[i+1] - prices[i]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))
        
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    @staticmethod
    def calculate_macd(prices: List[float], fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        if len(prices) < slow + signal:
            return None
        
        ema_fast = calculate_ema(prices, fast)
        ema_slow = calculate_ema(prices, slow)
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line (EMA of EMA)
        signal_ema = calculate_ema(prices[signal:], 9)
        
        if len(signal_ema) < signal:
            return None
        
        macd_cross = macd_line > signal_ema[-1] if ema_fast else None
        
        return {
            'macd_line': round(macd_line, 4),
            'signal_line': round(signal_ema, 4) if len(signal_ema) >= signal else None,
            'crosses_bullish': macd_cross
        }
    
    @staticmethod
    def calculate_ema(prices: List[float], period=20):
        """Calculate Exponential Moving Average"""
        weights = [period ** -1] + [1.0 / period * (i + 1) for i in range(period)]
        return sum(price * weight for price, weight in zip(prices, weights))
    
    @staticmethod
    def detect_trend_direction(prices: List[float], ma_period=50):
        """Determine overall trend direction"""
        if len(prices) < 2:
            return "UNKNOWN"
        
        prices_sorted = sorted(prices, reverse=True)
        current_idx = max(1, len(prices) - 1)
        lower_price = prices[current_idx - 1]
        upper_price = prices[current_idx + 1] if current_idx < len(prices) else None
        
        if not upper_price:
            return "DOWN"
        
        # Price above all moving averages = bullish
        if upper_price > (ma_period * prices_sorted[-2]) and lower_price < (ma_period * prices_sorted[-3]):
            return "UP"
        elif upper_price < (ma_period * prices_sorted[-2]) and lower_price > (ma_period * prices_sorted[-3]):
            return "DOWN"
        
        # Mixed signals = neutral
        return "NEUTRAL"

# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

class RecommendationEngine:
    """Generates buy/sell recommendations with profit potential scoring"""
    
    def __init__(self):
        self.engine = {
            'buys': [],  # Buy recommendations
            'sells': [], # Sell recommendations
            'neutral': []  # No-action positions
        }
        self.confidence_threshold = 0.35  # Minimum signal quality for inclusion
    
    def calculate_profit_score(self, entry_price: float, exit_price: Optional[float], 
                               current_rsi: int, current_trend: str) -> Tuple[int, str]:
        """Calculate profit potential score for a trading opportunity"""
        
        # Calculate potential profit
        if exit_price and exit_price > entry_price:
            potential_profit = (exit_price - entry_price) / entry_price
        else:
            return 0, "no_profit"
        
        # Score components
        rsi_position = self._calculate_rsi_score(current_rsi) if current_rsi else None
        
        # RSI score: Good in current trend, neutral otherwise
        if current_trend == "UP" and current_rsi < 70:
            rsi_bonus = min(rsi_position * 0.3, 50) if rsi_position else 0
        elif current_trend == "DOWN" and current_rsi > 30:
            rsi_bonus = min(rsi_position * 0.3, 40) if rsi_position else 0
        elif current_rsi is None or (current_rsi < 70 and current_trend != "UP"):
            rsi_bonus = 0
        
        # Trend alignment score
        trend_score = self._calculate_trend_score(current_trend, potential_profit > 0) if potential_profit else 0
        
        # Volume confirmation bonus
        volume_bonus = min(15, len(self.engine['buys']) * 2)  # Cap at 3 for first position
        
        total_score = rsi_bonus + trend_score + volume_bonus
        
        return int(total_score), f"RSI({current_rsi}, Trend={current_trend})"
    
    def _calculate_rsi_score(self, rsi: int) -> float:
        """Calculate RSI scoring component based on trend position"""
        if rsi < 30 and 'UP' in self.engine['buys']:
            return 10.0  # Oversold in uptrend = excellent signal
        elif rsi > 70 and 'DOWN' in self.engine['sells']:
            return 5.0  # Overbought but trend still down = cautious
        else:
            return min(6.0, (100 - abs(rsi)) * 0.1)  # Neutral position bonus
    
    def _calculate_trend_score(self, current_trend: str, has_profit_potential: bool) -> float:
        """Calculate how well trend aligns with entry"""
        if not has_profit_potential or current_trend != 'UP':
            return 0.0
        
        # Strong bullish alignment
        if current_trend == 'UP' and len(self.engine['buys']) >= 3:
            return 5.0
        
        # Mixed signals = neutral
        return 2.5

    def generate_recommendations(self, market_data: MarketData, 
                                  current_stock_price: float) -> Dict:
        """Generate comprehensive trading recommendations"""
        
        # Analyze index first for trend alignment
        self._analyze_market_trend(market_data, current_stock_price)
        
        # Generate buy/sell signals for each stock
        self._generate_stock_signals(current_stock_price)
        
        # Combine and score all signals
        scored_results = self.score_all_signals()
        
        return {
            'buys': scored_results['buys'],
            'sells': scored_results['sells'],
            'neutral': scored_results['neutral']
        }
    
    def _analyze_market_trend(self, market_data: MarketData, stock_price: float):
        """Analyze NIFTY/BANKNIFTY trend and apply to all stocks"""
        
        # Check if bullish for overall market
        nifty_current = market_data.index_data.get('NIFTY', {}).get('current_price')
        banknifty_current = market_data.index_data.get('BANKNIFTY', {}).get('current_price')
        
        if nifty_current and banknifty_current:
            bullish = (nifty_current > banknifty_current) or \
                     (nifty_current < banknifty_current * 1.023)
            
            if 'UP' in market_data.index_data['NIFTY'].get('trend', 'NEUTRAL'):
                bullish = True
        
        # Update all stocks based on trend
        for stock in self.engine['buys']:
            if stock['status'] != 'Awaiting analysis':  # Only analyze if pending
                update_score(stock, stock['current_price'], 'UP' if bullish else "DOWN", current_stock_price)

    def _generate_stock_signals(self, current_price: float):
        """Generate buy/sell signals for top stocks"""
        
        for i, stock in enumerate(self.engine['buys']):
            stock_score = self.calculate_profit_score(
                current_price, stock.get('exit_price'), 
                self.top_stocks[i]['rsi'] if hasattr(self.top_stocks[i], 'rsi') else 0,
                self.top_stocks[i]['trend']
            )
            
            score, reasoning = stock_score
            if score >= self.confidence_threshold:
                self.engine['buys'].append({
                    **stock,
                    'score': score,
                    'reasoning': reasoning
                })
        
        # Generate sell signals based on pullbacks and weakness
        self._generate_sell_positions(current_price)

    def score_all_signals(self) -> Dict:
        """Score all potential trades by profit potential"""
        
        scored_results = {
            'buys': [],  # Buy positions prioritized by potential return
            'sells': []   # Sell positions (less important than buys)
        }
        
        for stock in self.engine['buys']:
            score, reasoning = self.calculate_profit_score(
                stock['entry_price'], 
                stock.get('exit_price'),
                self.top_stocks[stock_idx]['rsi'] if hasattr(self.top_stocks[stock_idx], 'rsi') else 0,
                self.top_stocks[stock_idx]['trend']
            )
            
            if score >= self.confidence_threshold:
                scored_results['buys'].append({
                    **stock,
                    'profit_potential': score,
                    'reasoning': reasoning,
                    'risk': 5.0,
                    'action': 'ADD'
                })
        
        for i, stock in enumerate(self.engine['sells']):
            score, reasoning = self.calculate_profit_score(
                stock.get('exit_price'), 
                stock['current_price'],
                self.top_stocks[i]['rsi'] if hasattr(self.top_stocks[i], 'rsi') else 0,
                self.top_stocks[i]['trend']
            )
            
            if score >= self.confidence_threshold:
                scored_results['sells'].append({
                    **stock,
                    'profit_potential': score,
                    'reasoning': reasoning,
                    'risk': 3.0,
                    'action': 'REMOVE'
                })
        
        # Sort buy positions by profit potential (highest first)
        scored_results['buys'].sort(key=lambda x: x['profit_potential'], reverse=True)
        
        return scored_results

# ============================================================================
# USER INTERFACE & CONFIRMATION
# ============================================================================

class UserInterface:
    """Manages user input and display for trade recommendations"""
    
    def __init__(self):
        self.recommendations = []
        self.user_input = {}  # Store confirmed trades
    
    def create_daily_report(self, market_data: MarketData, 
                           technical_indicators: TechnicalIndicators) -> Dict:
        """Generate comprehensive daily market report"""
        
        report = {
            'date': date.today().isoformat(),
            'index_analysis': self._generate_index_report(market_data),
            'stock_analysis': self._generate_stock_analysis(market_data, technical_indicators),
            'overall_assessment': self._generate_overall_assessment()
        }
        
        return report
    
    def _generate_index_report(self, market_data: MarketData):
        """Generate NIFTY/BANKNIFTY market overview"""
        
        nifty = market_data.index_data.get('NIFTY', {})
        banknifty = market_data.index_data.get('BANKNIFTY', {})
        
        report = []
        report.append("=" * 60)
        report.append("DAILY MARKET OVERVIEW - INDIAN STOCKS")
        report.append("=" * 60)
        report.append("")
        
        # Index status
        if nifty.get('current_price'):
            report.append(f"📊 NIFTY 50: ₹{nifty['current_price']} (Current Price)")
            
            trend = nifty.get('trend', 'NEUTRAL')
            momentum = "BULLISH" if nifty['current_price'] > nifty['timestamp'] * 1.023 else "BEARISH"
            
            report.append(f"📈 Momentum: {momentum}")
            report.append("")
        else:
            report.append("❌ No current price data for NIFTY")
            report.append("")
        
        # BankNifty position
        if banknifty.get('current_price'):
            report.append(f"BANKNIFTY: ₹{banknifty['current_price']}")
            report.append("(Parallel to NIFTY)")
            report.append("")
        else:
            report.append("❌ No current price data for BANKNIFTY")
            report.append("")
        
        # Trend summary
        trend_text = f"Trend: {trend.upper()}" if nifty.get('current_price') else "Data not available"
        report.append(f"🎯 Overall Market Trend: {trend_text}")
        report.append("")
        
        return "\n".join(report)
    
    def _generate_stock_analysis(self, market_data: MarketData, 
                                 indicators: TechnicalIndicators):
        """Generate individual stock analysis"""
        
        report = []
        report.append("-" * 60)
        report.append("INDIVIDUAL STOCK ANALYSIS")
        report.append("-" * 60)
        report.append("")
        
        for idx, stock in enumerate(self.engine['buys'][:5]):  # Show top 5 buys only
            if not hasattr(stock, 'current_price'):
                continue
            
            stock_name = stock.get('name', f'Stock {idx}')
            entry_price = stock.get('entry_price')
            
            if not entry_price:
                continue
            
            rsi_str = f"RSI({stock['rsi']})" if hasattr(stock, 'rsi') else "N/A"
            
            report.append(f"{idx + 1}. {stock_name}")
            report.append(f"   Entry Price: ₹{entry_price:.2f} | Current: ₹{stock.get('current_price', 'N/A')}")
            report.append(f"   Indicators: {rsi_str}")
            report.append(f"   Score: {stock['score']} (Profit Potential)")
            report.append(f"   Trend: {stock.get('trend', 'N/A')}")
            report.append("")
        
        return "\n".join(report)

    def _generate_overall_assessment(self):
        """Generate overall market assessment"""
        
        report = []
        report.append("")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("📈 OVERALL MARKET ASSESSMENT")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        report.append(f"*Today's Market Status: {'UPTREND' if 'UP' in self.engine['buys'] else 'DOWNTREND' or 'STABLE'}")
        report.append("*NIFTY Trend: {'BULLISH' if 'UP' in self.engine['buys'] else 'BEARISH' or 'NEUTRAL'}")
        report.append("")
        
        # Summary score
        total_buy_score = sum(b.get('score', 0) for b in self.engine['buys'])
        avg_score = (total_buy_score / len(self.engine['buys'])) if self.engine['buys'] else 0
        
        report.append(f"💰 Total Buy Score: {int(total_buy_score)}")
        report.append(f"🎯 Average Score per Position: {avg_score:.1f}")
        report.append("")
        
        return "\n".join(report)

    def get_user_input(self, recommendations: Dict) -> Dict:
        """Get user input for trade execution"""
        
        print("\n" + "=" * 70)
        print("📊 DAILY TRADING RECOMMENDATIONS - FINAL SUMMARY")
        print("=" * 70)
        
        total_score = 0
        
        # Buy recommendations (sorted by profit potential)
        for i, pos in enumerate(recommendations['buys'][:5], 1):
            stock_name = next((s.get('name') or f'Stock {i}') for s in self.engine['buys'] if s['entry_price'] == pos['entry_price'])
            score = pos['score']
            
            print(f"\n{i}. BUY {stock_name}")
            print(f"   Entry: ₹{pos['entry_price']} | Target: ₹{(pos['exit_price'] or 100):.2f}")
            print(f"   Profit Score: {score}/100")
            
            # Ask user to confirm
            while True:
                confirm = input(f"\nAre you sure you want to trade this position? (y/n) ").strip().lower()
                if confirm in ['y', 'yes']:
                    break
                else:
                    print("Please confirm with 'y' or 'yes'")
        
        # Sell recommendations
        for i, pos in enumerate(recommendations['sells'][:3], 1):
            stock_name = next((s.get('name') or f'Stock {i}') for s in self.engine['buys'] if s.get('exit_price') == pos['entry_price'])
            
            print(f"\n{i}. SELL {stock_name}")
            print(f"   Entry Price: ₹{pos['current_price']} | Reason: Weakness pullback")
            print(f"   Score: {pos['score']}/100")
            
            confirm = input(f"\nAre you sure you want to take this position? (y/n) ").strip().lower()
            if confirm in ['y', 'yes']:
                self.user_input[pos['exit_price']] = 'SELL'
        
        return {
            'buys': pos_list,
            'sells': sell_list,
            'user_input': self.user_input.copy()
        }

    def update_user_input(self, stock_name: str, action: str):
        """Update user input based on their confirmation"""
        
        if stock_name in self.user_input and self.user_input[stock_name] == 'NONE':
            self.user_input[stock_name] = action
    
    def show_confirmations(self, recommendations: Dict, stock_data: MarketData) -> None:
        """Show final confirmations for all trade decisions"""
        
        print("\n" + "=" * 70)
        print("✅ CONFIRMATION SCREEN - TRADE DECISIONS")
        print("=" * 70)
        print(f"\n📅 Date: {date.today().strftime('%Y-%m-%d')}")
        print(f"🏦 Market Trend: {'UPTREND' if 'UP' in self.engine['buys'] else (f'DOWN' if stock_data.index_data.get('BANKNIFTY', {}).get('current_price') and 'DOWN' in stock_data.index_data['BANKNIFTY'].get('trend', '') else 'UNKNOWN')}")
        print("=" * 70)
        
        # Show buy positions
        buy_count = sum(1 for b in self.engine['buys'] if b['entry_price'] is not None and b['exit_price'] is not None)
        print(f"\n💰 BUY PORTFOLIO ({buy_count} position(s))")
        print("   " + "-" * 70)
        
        for pos in recommendations['buys']:
            stock_name = next((s.get('name') or f'Stock {pos["entry_price"]}') 
                            for s in self.engine['buys'] if s['entry_price'] == pos['entry_price'])
            
            print(f"\n   Position #{len(recommendations['buys'])}")
            print(f"   Stock: {stock_name} | Price: ₹{pos['entry_price']}")
            print(f"   Entry: ₹{pos['entry_price']} | Exit: ₹{(pos['exit_price'] or 'N/A')}")
            
            # Confirm action (BUY or SELL)
            if pos['action'] == 'ADD':
                confirmation = input(f"\n   ACTION: BUY this position? (y/n) ").strip().lower()
            elif pos['action'] == 'REMOVE':
                confirmation = input(f"\n   ACTION: REMOVE from portfolio? (y/n) ").strip().lower()
        
            if confirmation in ['y', 'yes']:
                if pos['action'] == 'ADD':
                    self.user_input[pos['entry_price']] = 'BUY'
                    print("   ✓ CONFIRMED: Adding BUY position")
                else:
                    self.user_input[pos['exit_price']] = 'SELL'
                    print("   ✓ CONFIRMED: Removing from portfolio")

        # Show sell positions
        print("\n\n💰 SELL/REMOVE PORTFOLIO (" + str(len(recommendations['sells']) if recommendations['buys'] else "0") + ") position(s)")
        print("   " + "-" * 70)
        
        for pos in recommendations['sells']:
            stock_name = next((s.get('name') or f'Stock {pos["exit_price"]}') 
                            for s in self.engine['buys'] if s.get('exit_price') == pos['entry_price'])
            
            print(f"\n   Position #{len(recommendations['sells'])}")
            print(f"   Stock: {stock_name} | Price: ₹{pos['current_price']}")
            
            # Confirm action
            confirmation = input(f"\n   ACTION: SELL this position? (y/n) ").strip().lower()
        
        if confirmation in ['y', 'yes']:
            print("   ✓ CONFIRMED: Taking SELL position")

        print("\n" + "=" * 70)
        print("📋 EXECUTION SUMMARY")
        print("=" * 70)
        print(f"✅ BUY positions to add: {[p['entry_price'] for p in recommendations['buys'] if p.get('action') == 'ADD']}")
        print(f"✅ SELL positions to take: {[p['exit_price'] for p in recommendations['sells'] if p.get('action') == 'REMOVE']}")
        print("⚠️  User must confirm each position BEFORE execution")

def main():
    """Main entry point for the Indian Market Trading Agent"""
    
    print("\n" + "=" * 70)
    print("🚀 INDIAN MARKET TRADING AGENT - INITIAL SETUP")
    print("=" * 70)
    
    # Initialize data structures
    market_data = MarketData()
    technical_indicators = TechnicalIndicators()
    recommendation_engine = RecommendationEngine()
    user_interface = UserInterface()
    
    # Get current market status
    today = date.today().isoformat()
    print(f"\n📅 Today's Date: {today}")
    
    # Check for any existing price data
    nifty_data = MarketData().update(19500.0, 'UP')  # Mock initial update
    banknifty_data = MarketData().update(18400.0, 'UP')  # Mock initial update
    
    # Get stock analysis
    print("\n📊 Analyzing Indian market stocks with technical indicators...")
    
    recommendations = recommendation_engine.generate_recommendations(market_data, 20000.0)
    current_price = recommendations['buys'][0]['entry_price'] if recommendations['buys'] else None
    
    # Show report to user
    print("\n" + "=" * 70)
    print("📊 DAILY MARKET ANALYSIS - TECHNICAL INDICATORS")
    print("=" * 70)
    
    daily_report = user_interface.create_daily_report(market_data, technical_indicators)
    print(daily_report)
    
    # Generate user input for execution
    print("\n🎯 FINAL TRADING RECOMMENDATIONS (User Confirmation Required)")
    
    confirmed_input = user_interface.get_user_input(recommendations)
    
    # Show summary with current market data
    print(f"\n💵 Current Market Data:")
    if current_price:
        nifty_current = market_data.index_data['NIFTY']['current_price']
        banknifty_current = market_data.index_data['BANKNIFTY']['current_price']
        
        print(f"   NIFTY 50: ₹{nifty_current:.2f}")
        print(f"   BANKNIFTY: ₹{banknifty_current:.2f} ({(nifty_current/banknifty_current * 100):.1f}% of NIFTY)")
        
        # Analyze individual stocks
        for i, pos in enumerate(confirm_input['buys'][:5], 1):
            if pos.get('action') == 'ADD' and pos.get('entry_price'):
                stock_name = next((s.get('name') or f'Stock {pos["entry_price"]}') 
                                for s in market_data.top_stocks if s['entry_price'] == pos['entry_price'])
                
                print(f"\n   BUY #{i}: {stock_name}")
                print(f"      Entry: ₹{pos['entry_price']} | Score: {pos.get('score', 'N/A')}")

    print("\n📝 USER INSTRUCTIONS:")
    print("-" * 70)
    print("✅ All BUY positions must be explicitly confirmed before execution")
    print("   - Type 'y' to confirm adding position")
    print("   - Type 'n' or skip for not trading this position")
    print("\n📋 SELL/REMOVE positions are also confirmed above")
    print("-" * 70)

if __name__ == "__main__":
    main()
