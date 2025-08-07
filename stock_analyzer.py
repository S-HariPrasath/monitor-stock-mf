import yfinance as yf
import pandas as pd
import numpy as np
import warnings
from datetime import datetime
from config import (
    SIGNAL_WEIGHTS, RSI_PERIOD, SMA_20_PERIOD, SMA_50_PERIOD, SMA_200_PERIOD,
    EMA_12_PERIOD, EMA_26_PERIOD, MACD_SIGNAL_PERIOD, BB_PERIOD, BB_STD_MULTIPLIER,
    VOLUME_AVG_PERIOD, VOLUME_SPIKE_MULTIPLIER, RSI_OVERSOLD, STOCK_DATA_PERIOD
)

warnings.filterwarnings('ignore')


class LongTermStockMonitor:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_stock_data(self, period=STOCK_DATA_PERIOD):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(self.symbol)
            data = stock.history(period=period)
            if data.empty:
                print(f"No data found for {self.symbol}")
                return None
            return data
        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")
            return None

    def calculate_technical_indicators(self, df):
        """Calculate various technical indicators"""
        if df is None or df.empty:
            return None

        # Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=SMA_20_PERIOD).mean()
        df['SMA_50'] = df['Close'].rolling(window=SMA_50_PERIOD).mean()
        df['SMA_200'] = df['Close'].rolling(window=SMA_200_PERIOD).mean()
        df['EMA_12'] = df['Close'].ewm(span=EMA_12_PERIOD).mean()
        df['EMA_26'] = df['Close'].ewm(span=EMA_26_PERIOD).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=MACD_SIGNAL_PERIOD).mean()

        # RSI
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=RSI_PERIOD).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=RSI_PERIOD).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=BB_PERIOD).mean()
        bb_std = df['Close'].rolling(window=BB_PERIOD).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * BB_STD_MULTIPLIER)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * BB_STD_MULTIPLIER)

        # Volume
        df['Volume_Avg20'] = df['Volume'].rolling(window=VOLUME_AVG_PERIOD).mean()

        return df

    def generate_signals(self, df):
        """Generate trading signals based on technical indicators"""
        if df is None or df.empty:
            return {}

        signals = {}
        current = df.iloc[-1]
        previous = df.iloc[-2]

        # Moving Average Crossovers
        if current['SMA_20'] > current['SMA_50'] and previous['SMA_20'] <= previous['SMA_50']:
            signals['MA_Crossover'] = "Golden Cross: 20 SMA > 50 SMA"

        if current['EMA_12'] > current['EMA_26'] and previous['EMA_12'] <= previous['EMA_26']:
            signals['EMA_Crossover'] = "EMA Golden Cross: 12 EMA > 26 EMA"

        # MACD Signals
        if current['MACD'] > current['MACD_Signal'] and previous['MACD'] <= previous['MACD_Signal']:
            signals['MACD_Bullish'] = "MACD crossed above signal"

        if current['MACD'] > 0 and previous['MACD'] <= 0:
            signals['MACD_Positive'] = "MACD turned positive"

        # RSI Signals
        if current['RSI'] <= RSI_OVERSOLD:
            signals['RSI_Oversold'] = f"RSI Oversold ({current['RSI']:.2f})"

        # Bollinger Band Signals
        if current['Close'] < current['BB_Lower']:
            signals['BB_Oversold'] = "Price below lower Bollinger Band"

        # Volume Signals
        if current['Volume'] > current['Volume_Avg20'] * VOLUME_SPIKE_MULTIPLIER:
            signals['High_Volume'] = f"Volume spike > {VOLUME_SPIKE_MULTIPLIER}x average"

        # Trend Signals
        if current['Close'] > current['SMA_200'] and current['SMA_20'] > current['SMA_50']:
            signals['Uptrend'] = "Long-term uptrend in place"

        return signals

    def score_signals(self, signals):
        """Calculate signal strength score (0-100)"""
        if not signals:
            return 0

        return min(sum(SIGNAL_WEIGHTS.get(sig, 0) for sig in signals), 100)

    def analyze(self):
        """Complete stock analysis"""
        data = self.get_stock_data()
        if data is None:
            return None

        df = self.calculate_technical_indicators(data)
        if df is None:
            return None

        signals = self.generate_signals(df)
        score = self.score_signals(signals)
        current_price = df['Close'].iloc[-1]
        date = df.index[-1].strftime('%Y-%m-%d')

        return {
            'symbol': self.symbol,
            'date': date,
            'price': current_price,
            'score': score,
            'signals': signals,
            'rsi': df['RSI'].iloc[-1],
            'macd': df['MACD'].iloc[-1],
            'sma_20': df['SMA_20'].iloc[-1],
            'sma_50': df['SMA_50'].iloc[-1],
            'sma_200': df['SMA_200'].iloc[-1],
            'bb_lower': df['BB_Lower'].iloc[-1]
        }


def get_recommendation(score):
    """Get recommendation based on signal score"""
    from config import STRONG_BUY_THRESHOLD, MODERATE_BUY_THRESHOLD, WEAK_BUY_THRESHOLD
    
    if score >= STRONG_BUY_THRESHOLD:
        return "STRONG BUY"
    elif score >= MODERATE_BUY_THRESHOLD:
        return "MODERATE BUY"
    elif score >= WEAK_BUY_THRESHOLD:
        return "WEAK BUY / VALUE ENTRY"
    else:
        return "HOLD / NO ACTION"


def print_stock_analysis(result, name):
    """Print formatted stock analysis to console"""
    if not result:
        print("⚠️ Data unavailable.")
        return

    print(f"📅 Date: {result['date']}")
    print(f"💰 Current Price: ₹{result['price']:.2f}")
    print(f"📊 Signal Strength: {result['score']}/100")

    recommendation = get_recommendation(result['score'])
    if result['score'] >= 70:
        print("🎯 RECOMMENDATION: STRONG BUY")
    elif result['score'] >= 50:
        print("✅ RECOMMENDATION: MODERATE BUY")
    elif result['score'] >= 30:
        print("💡 RECOMMENDATION: WEAK BUY / VALUE ENTRY")
    else:
        print("❌ RECOMMENDATION: HOLD / NO ACTION")

    print(f"\n✅ Detected Signals:")
    if result['signals']:
        for desc in result['signals'].values():
            print(f"   • {desc}")
    else:
        print("   No active signals.")

    print(f"\n📈 Key Indicators:")
    print(f"   RSI: {result['rsi']:.2f}")
    print(f"   MACD: {result['macd']:.4f}")
    print(f"   20-day SMA: ₹{result['sma_20']:.2f}")
    print(f"   50-day SMA: ₹{result['sma_50']:.2f}")
    print(f"   200-day SMA: ₹{result['sma_200']:.2f}")
    print(f"   Bollinger Lower Band: ₹{result['bb_lower']:.2f}")
