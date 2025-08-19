# 🇮🇳 Indian Market Monitor

A simple program to monitor Indian stock market (Nifty 50 & Sensex) and send Telegram alerts when the market is down.

## What it monitors:
- ✅ Nifty 50 drops more than 2% in a day
- ✅ Both Sensex and Nifty are in red
- ✅ Market opens gap down by more than 1%

## 🚀 Deploy to Render (FREE)

### Quick Setup

1. **Fork/Clone this repository**
2. **Go to [Render.com](https://render.com)**
3. **Sign up with GitHub**
4. **Click "New" → "Web Service"**
5. **Connect your GitHub repository**
6. **Set Environment Variables:**
   - `TELEGRAM_BOT_TOKEN`: `telegram_bot_token`
   - `TELEGRAM_CHAT_ID`: `telegram_chat_id`
7. **Deploy!**

### How it works

The program:
1. Runs continuously 24/7 on Render
2. Checks market every 5 minutes during market hours (9:15 AM - 3:30 PM IST)
3. Fetches real-time Nifty 50 and Sensex data from Yahoo Finance
4. Sends Telegram alerts when conditions are met
5. Provides health check dashboard

### Sample Alert
```
🇮🇳 Indian Market Alert
⏰ 2024-08-19 14:30:00

Market Status:
Nifty 50: 19,450.25 (-2.15%)
Sensex: 64,200.50 (-1.85%)

🚨 Alerts:
• 🚨 Nifty 50 down -2.15% (more than 2%)
• 📉 Both indices in red: Nifty -2.15%, Sensex -1.85%
• ⚡ Market gap down: Nifty -2.15%

Overall Market Sentiment: 🔴 BEARISH

Alert from Render Market Monitor
```

## Files
- `market_monitor_render.py` - Main monitoring script
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies
- `config.json` - Local configuration (not used in Render)
- `README.md` - This file

## Features
- Real-time market data from Yahoo Finance
- Telegram alerts with formatted messages
- Health check dashboard at `/health`
- Automatic market hours detection
- Continuous monitoring 24/7
- Configurable thresholds

## Monitoring Dashboard

### Health Check
Visit `your-app.onrender.com/health` to see:
- Service status
- Last market check time
- Last alert sent time
- Market open/closed status

### Render Dashboard
- View logs in real-time
- Monitor resource usage
- Automatic deployments on code changes

## Cost
- **Render**: $0 (750 hours/month free)
- **Telegram Bot**: $0 (unlimited)
- **Market Data**: $0 (Yahoo Finance API)

**Total Cost: $0** 🎉

## Troubleshooting

### Common Issues
1. **"Missing Telegram credentials"**
   - Check environment variables in Render dashboard
   - Verify bot token and chat ID

2. **"Failed to fetch market data"**
   - Usually temporary network issue
   - Will retry automatically in 5 minutes

3. **Service not starting**
   - Check logs in Render dashboard
   - Verify requirements.txt is correct

### Logs
- Check Render dashboard for detailed logs
- Each check shows market data and alert status

Perfect for monitoring Indian markets without spending anything! 🚀
