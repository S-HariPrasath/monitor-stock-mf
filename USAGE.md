# Stock Monitor Usage Guide

## 📁 Project Structure

```
mf_stock_monitor/
├── monitor_stock_mf.py      # Main application entry point
├── config.py               # Configuration settings
├── stock_analyzer.py       # Stock analysis functionality
├── telegram_bot.py         # Telegram bot functionality
├── scheduler.py            # Scheduling and monitoring
├── requirements.txt        # Python dependencies
├── Procfile               # Railway deployment config
├── runtime.txt            # Python version
├── README.md              # Project overview
├── TELEGRAM_SETUP.md      # Telegram setup guide
└── USAGE.md               # This file
```

## 🚀 How to Use

### 1. Single Analysis (One-time run)
```bash
python monitor_stock_mf.py --single
```
This runs a one-time analysis of all stocks and displays results in the console.

### 2. Continuous Monitoring (Production)
```bash
python monitor_stock_mf.py
```
This starts continuous monitoring with:
- Daily reports at 1:00 PM IST (trading days only)
- Real-time Telegram alerts for strong signals
- Automatic scheduling and error recovery

## ⚙️ Configuration

### Edit `config.py` to customize:

#### Stock Symbols
```python
STOCK_SYMBOLS = {
    'SUNPHARMA.NS': 'Sunpharma',
    'HDFCBANK.NS': 'HDFC Bank',
    # Add more stocks here
}
```

#### Alert Thresholds
```python
ALERT_THRESHOLD = 50        # Send alerts for scores >= 50
STRONG_BUY_THRESHOLD = 70   # Strong buy threshold
MODERATE_BUY_THRESHOLD = 50 # Moderate buy threshold
WEAK_BUY_THRESHOLD = 30     # Weak buy threshold
```

#### Daily Report Time
```python
DAILY_REPORT_TIME = "13:00"  # 1:00 PM IST
```

#### Technical Indicators
```python
RSI_PERIOD = 14              # RSI calculation period
SMA_20_PERIOD = 20          # 20-day SMA
SMA_50_PERIOD = 50          # 50-day SMA
# ... and more
```

## 🔧 Customization Examples

### Add New Stocks
1. Edit `config.py`
2. Add new symbols to `STOCK_SYMBOLS`
3. Redeploy or restart

### Change Alert Threshold
1. Edit `ALERT_THRESHOLD` in `config.py`
2. Restart the application

### Modify Signal Weights
1. Edit `SIGNAL_WEIGHTS` in `config.py`
2. Adjust weights for different signals
3. Restart the application

### Change Daily Report Time
1. Edit `DAILY_REPORT_TIME` in `config.py`
2. Use 24-hour format (e.g., "14:30" for 2:30 PM)
3. Restart the application

## 📊 Understanding the Output

### Signal Score Legend
- **70-100**: Strong Buy 🎯
- **50-69**: Moderate Buy ✅
- **30-49**: Weak Buy 💡
- **0-29**: Hold ❌

### Technical Indicators
- **RSI**: Relative Strength Index (0-100)
- **MACD**: Moving Average Convergence Divergence
- **SMA**: Simple Moving Average
- **EMA**: Exponential Moving Average
- **BB**: Bollinger Bands

### Signals Detected
- **Golden Cross**: 20 SMA > 50 SMA
- **EMA Crossover**: 12 EMA > 26 EMA
- **MACD Bullish**: MACD crossed above signal
- **RSI Oversold**: RSI ≤ 30
- **Volume Spike**: Volume > 1.5x average
- **Uptrend**: Price > 200 SMA and 20 SMA > 50 SMA

## 🛠️ Troubleshooting

### Common Issues

#### Import Errors
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

#### Telegram Not Working
1. Check environment variables
2. Verify bot token and chat ID
3. Ensure bot is started in Telegram

#### No Data Received
1. Check internet connection
2. Verify stock symbols are correct
3. Check yfinance API status

#### Scheduling Issues
1. Verify timezone settings
2. Check if it's a trading day
3. Look at application logs

## 📱 Telegram Features

### Daily Report (1:00 PM IST)
- Market summary with counts
- Individual stock analysis
- Sorted by signal strength
- Key indicators for each stock

### Real-time Alerts
- Instant notifications for strong signals
- Formatted with emojis and HTML
- Includes key indicators and signals

## 🔄 Deployment

### Railway Deployment
1. Push code to GitHub
2. Connect to Railway
3. Add environment variables
4. Monitor logs

### Local Development
1. Set environment variables
2. Run with `python monitor_stock_mf.py`
3. Test with `--single` flag

## 📈 Monitoring

### Logs to Watch
- Application startup
- Daily report generation
- Telegram message delivery
- Error messages

### Key Metrics
- Signal scores for each stock
- Alert frequency
- Report delivery success
- Error rates

---

**Need help?** Check the logs, verify configuration, and ensure all dependencies are installed correctly.
