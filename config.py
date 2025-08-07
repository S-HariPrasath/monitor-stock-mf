# Stock symbols to monitor
STOCK_SYMBOLS = {
    'SUNPHARMA.NS': 'Sunpharma',
    'HDFCBANK.NS': 'HDFC Bank',
    'TATASTEEL.NS': 'Tata Steel',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'TATAMOTORS.NS': 'Tata Motors',
    '^NSEI': 'Nifty 50'
}

# Signal weights for scoring
SIGNAL_WEIGHTS = {
    'MA_Crossover': 20,
    'EMA_Crossover': 15,
    'MACD_Bullish': 12,
    'MACD_Positive': 8,
    'RSI_Oversold': 25,
    'BB_Oversold': 20,
    'High_Volume': 10,
    'Uptrend': 15
}

# Alert thresholds
ALERT_THRESHOLD = 50  # Send alerts for scores >= 50
STRONG_BUY_THRESHOLD = 70
MODERATE_BUY_THRESHOLD = 50
WEAK_BUY_THRESHOLD = 30

# Scheduling settings
DAILY_REPORT_TIME = "13:00"  # 1:00 PM IST
TIMEZONE = "Asia/Kolkata"

# Trading hours settings (IST)
TRADING_START_HOUR = 9
TRADING_START_MINUTE = 15
TRADING_END_HOUR = 15
TRADING_END_MINUTE = 30

# Data settings
STOCK_DATA_PERIOD = "1y"  # 1 year of historical data

# Technical indicator settings
RSI_PERIOD = 14
SMA_20_PERIOD = 20
SMA_50_PERIOD = 50
SMA_200_PERIOD = 200
EMA_12_PERIOD = 12
EMA_26_PERIOD = 26
MACD_SIGNAL_PERIOD = 9
BB_PERIOD = 20
BB_STD_MULTIPLIER = 2
VOLUME_AVG_PERIOD = 20
VOLUME_SPIKE_MULTIPLIER = 1.5

# RSI thresholds
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
