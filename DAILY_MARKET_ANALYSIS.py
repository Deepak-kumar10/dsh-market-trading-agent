"""
Daily Market Analysis Report Generator

Generates comprehensive daily market recommendations with technical analysis.
Shows both demo (mock data) and production results side-by-side for comparison.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# ============================================================================
# MARKET DATA FETCHING
# ============================================================================

def fetch_nifty_current_price() -> Optional[float]:
    """Fetch current NIFTY price from NSE API"""
    try:
        headers = {'apikey': 'demo_key'}  # Demo mode key
        response = requests.get(
            "https://www.nseindia.com/api/prices/candle",
            headers=headers
        )
        
        if response.status_code == 200:
            candles = [c for c in response.json()['candles'] 
                      if 'close' in c and len(c) >= 5]
            
            if candles:
                return float(candles[0]['close'])
        
        return None
    except Exception as e:
        print(f"Error fetching NIFTY price: {e}")
        return None

def fetch_banknifty_current_price() -> Optional[float]:
    """Fetch current BANKNIFTY price from NSE API"""
    try:
        headers = {'apikey': 'demo_key'}
        response = requests.get(
            "https://www.nseindia.com/api/index/50",
            headers=headers
        )
        
        if response.status_code == 200:
            index_50_data = response.json()
            current_price = index_50_data.get('index_50', {}).get('current_price', None)
            
            if current_price:
                return current_price
        
        return None
    except Exception as e:
        print(f"Error fetching BANKNIFTY price: {e}")
        return None

def fetch_nifty_trend() -> Optional[str]:
    """Determine NIFTY trend direction"""
    nifty_price = fetch_nifty_current_price()
    
    if nifty_price and len(candles := get_recent_nifty_candles(50)) > 1:
        recent_prices = [c['close'] for c in candles]
        current_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100
        
        if current_change > 3:
            return 'UP'
        elif current_change < -3:
            return 'DOWN'
    
    return None

def fetch_banknifty_trend() -> Optional[str]:
    """Determine BANKNIFTY trend direction"""
    banknifty_price = fetch_banknifty_current_price()
    
    if banknifty_price and len(candles := get_recent_banknifty_candles(50)) > 1:
        recent_prices = [c['close'] for c in candles]
        current_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100
        
        if current_change > 3:
            return 'UP'
        elif current_change < -3:
            return 'DOWN'
    
    return None

def fetch_nifty_rsi() -> Optional[int]:
    """Calculate RSI for NIFTY"""
    try:
        from dsh_indicators import calculate_rsi
        
        price = fetch_nifty_current_price()
        
        if price and len(candles := get_recent_nifty_candles(50)) > 14:
            prices = [c['close'] for c in candles]
            return int(calculate_rsi(prices, period=14))
    
    except ImportError as e:
        print(f"RSI not available: {e}")
    except Exception as e:
        print(f"Error calculating RSI: {e}")
    
    return None

def fetch_nifty_macd() -> Optional[Dict]:
    """Calculate MACD for NIFTY"""
    try:
        from dsh_indicators import calculate_macd, calculate_ema
        
        price = fetch_nifty_current_price()
        
        if price and len(candles := get_recent_nifty_candles(50)) > 12:
            candles = [c['close'] for c in candles]
            ema_fast = calculate_ema(candles[:12], 12)
            ema_slow = calculate_ema(candles[:12], 26)
            macd_line = ema_fast[0] - ema_slow[0]
            
            signal_ema = calculate_ema(candles[12:], 9)[0]
            
            return {
                'macd_line': round(macd_line, 4),
                'signal_line': round(signal_ema, 4),
                'crosses_bullish': True  # Placeholder for demo
            }
    
    except Exception as e:
        print(f"Error calculating MACD: {e}")
    
    return None

def get_recent_nifty_candles(end_date: Optional[datetime] = None, days: int = 60) -> List[Dict]:
    """Get recent NIFTY price candles"""
    try:
        if end_date:
            date_str = end_date.strftime("%Y-%m-%dT%H:%M")
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            date_str = f"{today}T12:00"
        
        url = "https://www.nseindia.com/api/prices/candle"
        
        if '/candles' not in date_str and 'STOCK_ID' in date_str:
            parts = date_str.split('/')
            stock_id = parts[4] if len(parts) > 4 else None
            
            url += f"?stock_id={stock_id}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            candles = [item for item in response.json()['candles'] if 'close' in item]
            return candles
        
        return []
    
    except Exception as e:
        print(f"Error fetching NIFTY history: {e}")
        return []

def get_recent_banknifty_candles(end_date: Optional[datetime] = None, days: int = 60) -> List[Dict]:
    """Get recent BANKNIFTY price candles"""
    try:
        if end_date:
            date_str = end_date.strftime("%Y-%m-%dT%H:%M")
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            date_str = f"{today}T12:00"
        
        url = "https://www.nseindia.com/api/prices/candle"
        
        if '/candles' not in date_str and 'STOCK_ID' in date_str:
            parts = date_str.split('/')
            stock_id = parts[4] if len(parts) > 4 else None
            
            url += f"?stock_id={stock_id}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            candles = [item for item in response.json()['candles'] if 'close' in item]
            return candles
        
        return []
    
    except Exception as e:
        print(f"Error fetching BANKNIFTY history: {e}")
        return []

# ============================================================================
# SCORING ENGINE
# ============================================================================

class WinningScoreScoringClass:
    """Production scoring implementation for buy/sell signals"""
    
    def __init__(self, market_data):
        self.market = market_data
        self.stock_candidates = [
            'Tata Steel',
            'Reliance Industries', 
            'HDFC Bank',
            'ICICI Bank',
            'Infosys',
            'L&T Technologies'
        ]
        
    def score_stock(self, name: str, price: float, trend: Optional[str], rsi: Optional[int]) -> int:
        """Score a single stock position"""
        score = 0
        
        # Trend alignment score (15 points max)
        if trend == 'UP':
            score += min(15, 3)  # Bonus for stocks in uptrend
        
        # RSI position bonus
        if rsi and rsi < 30:
            score += 5  # Oversold = buy signal
        elif rsi and rsi > 70:
            score -= 2  # Overbought = avoid
        elif rsi is None or (not trend == 'UP' and rsi is None):
            score += 2  # Neutral position
        
        return max(0, min(100, score))

# ============================================================================
# RECOMMENDATION GENERATOR
# ============================================================================

def generate_recommendations() -> Dict:
    """Generate comprehensive market recommendations"""
    
    print("=" * 70)
    print("📊 DAILY MARKET ANALYSIS - PRODUCTION RESULTS")
    print("=" * 70)
    
    # Fetch market data
    nifty_price = fetch_nifty_current_price()
    banknifty_price = fetch_banknifty_current_price()
    nifty_trend = fetch_nifty_trend()
    banknifty_trend = fetch_banknifty_trend()
    nifty_rsi = fetch_nifty_rsi()
    
    print("\n📈 CURRENT MARKET PRICES:")
    if nifty_price:
        print(f"   NIFTY 50: ₹{nifty_price:.2f}")
    else:
        print("   NIFTY 50: Unable to fetch (Demo mode)")
    
    print(f"\n📊 CURRENT INDICES:")
    if banknifty_price and nifty_price:
        bank_factor = nifty_price / banknifty_price * 100
        print(f"   BANKNIFTY: ₹{banknifty_price:.2f} ({bank_factor:.1f}% of NIFTY)")
    
    print("\n📈 CURRENT TRENDS:")
    if nifty_trend and (banknifty_trend or True):
        trend_text = "IN PARALLEL" if nifty_trend == banknifty_trend else "SIMPLE ALIGNMENT"
        print(f"   • NIFTI {nifty_trend.upper()}")
    elif nifty_price:
        print("   • NIFTI: Checking trends...")
    
    if banknifty_price:
        print(f"   • BANKNIFTY: {banknifty_trend.upper()}" if banknifty_trend else "   • BANKNIFTY: Unable to fetch")

# ============================================================================
# DEMO MODE OUTPUT (for comparison)
# ============================================================================

def run_demo_mode_comparison():
    """Run agent in demo mode and generate comparison report"""
    
    print("\n⚠️  DEMO MODE - MOCK DATA MODE")
    print("=" * 70)
    print("This is running with mock prices - COMPARISON WITH PRODUCTION MODE")
    print("=" * 70)
    
    # Simulate demo data for comparison
    print("\n📊 DEMO MODE RECOMMENDATIONS:")
    print("-" * 70)
    print("╔═══════════════════════════════════════════════════╗")
    print("║  📊 DAILY MARKET ANALYSIS - MOCK DATA            ║")
    print("╠═══════════════════════════════════════════════════╣")
    print("║  NIFTY 50: ₹19,500.00                           ║")
    print("║  BANKNIFTY: ₹18,450.00                         ║")
    print("║  (Current Prices - Simulated for Demo Mode)     ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    print("\n📈 MARKET TRENDS (Simulated):")
    print("-" * 70)
    print("   • NIFTI UPTREND - Momentum detected")
    print("   • BANKNIFTY: IN PARALLEL (2.3% lag)")
    print("   • Overall Market: BULLISH")

def run_production_mode_analysis():
    """Show production-ready analysis structure"""
    
    print("\n📊 PRODUCTION MODE RECOMMENDATION STRUCTURE:")
    print("-" * 70)
    print("Production analysis framework uses live market data; demo mode uses mock sample prices.")
    print("-" * 70)

def generate_report():
    """Generate complete daily analysis report"""
    
    print("\n📊 DAILY MARKET ANALYSIS - PRODUCTION REPORT")
    print("=" * 70)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # Market Analysis Summary
    print("\n📊 MARKET OVERVIEW")
    print("-" * 70)
    print("Daily market recommendations report template.")
    
    print("No scored positions are available in this report template.")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run full analysis"""
    
    # Fetch market data
    nifty_price = fetch_nifty_current_price()
    banknifty_price = fetch_banknifty_current_price()
    nifty_trend = fetch_nifty_trend()
    banknifty_trend = fetch_banknifty_trend()
    nifty_rsi = fetch_nifty_rsi()
    
    print("=" * 70)
    print("🚀 INDIAN MARKET TRADING AGENT - LIVE DATA REPORT")
    print("=" * 70)
    
    # Display current market data
    if nifty_price:
        print(f"\n📊 NIFTY 50 CURRENT PRICE: ₹{nifty_price:.2f}")
    else:
        print("\n⚠️  NIFTY 50: Unable to fetch live price")
    
    if banknifty_price:
        bank_factor = nifty_price / banknifty_price * 100 if nifty_price and banknifty_price else None
        print(f"   BANKNIFTY CURRENT PRICE: ₹{banknifty_price:.2f} ({bank_factor:.1f}% of NIFTY)")
    else:
        print("\n⚠️  BANKNIFTY: Unable to fetch live price")
    
    print("\n📈 MARKET TRENDS:")
    if nifty_trend and (banknifty_trend or True):
        text = "IN PARALLEL" if nifty_trend == banknifty_trend else "SIMPLE ALIGNMENT"
        print(f"   • NIFTI: {nifty_trend.upper()}")
        print(f"   • BANKNIFTY: {banknifty_trend.upper()}" if banknifty_trend else "")
    elif nifty_trend:
        print(f"   • NIFTI: {nifty_trend.upper()}")

# ============================================================================
# DEMO MODE COMPARISON
# ============================================================================

def main():
    """Main execution for demo mode comparison"""
    
    # Run demo mode analysis
    run_demo_mode_comparison()
    
    # Generate full report with mock data
    generate_report()
    
    print("\n✅ Demo mode complete - Use Production Mode with API credentials for live data")

if __name__ == "__main__":
    main()
