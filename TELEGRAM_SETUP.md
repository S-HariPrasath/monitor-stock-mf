# Telegram Bot Setup Guide

## 🚀 How to Set Up Telegram Alerts for Your Stock Monitor

### Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather
3. **Send the command**: `/newbot`
4. **Follow the instructions**:
   - Enter a name for your bot (e.g., "Stock Monitor Bot")
   - Enter a username (must end with 'bot', e.g., "my_stock_monitor_bot")
5. **Save the bot token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your Chat ID

#### Method 1: Using @userinfobot
1. Search for `@userinfobot` in Telegram
2. Start a chat with it
3. It will reply with your Chat ID (a number like `123456789`)

#### Method 2: Using your bot
1. Start a chat with your bot
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the "chat" object and find your "id"

### Step 3: Configure Environment Variables

#### For Local Testing:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

#### For Railway Deployment:
1. Go to your Railway project dashboard
2. Click on **"Variables"** tab
3. Add these environment variables:
   - `TELEGRAM_BOT_TOKEN` = your bot token
   - `TELEGRAM_CHAT_ID` = your chat ID

### Step 4: Test Your Bot

1. **Run your script locally**:
   ```bash
   python monitor_stock_mf.py
   ```

2. **Check Telegram** for alerts when stocks have strong signals (score ≥ 50)

### Step 5: Deploy to Railway

1. **Push your updated code** to GitHub
2. **Railway will automatically redeploy** with the new Telegram functionality
3. **Add environment variables** in Railway dashboard
4. **Monitor logs** to see Telegram alerts

## 📱 What You'll Receive

### 🕐 Daily Report (1:00 PM IST, Trading Days Only):
```
📊 DAILY STOCK MARKET REPORT
📅 Date: 2024-01-15 13:00 IST

==================================================

📈 MARKET SUMMARY:
🎯 Strong Buy: 2 stocks
✅ Moderate Buy: 1 stocks  
💡 Weak Buy: 2 stocks
❌ Hold: 1 stocks

==================================================

🎯 Sunpharma (SUNPHARMA.NS)
💰 Price: ₹1,234.56 | 📊 Score: 85/100
🎯 STRONG BUY

📈 Indicators:
• RSI: 25.30
• MACD: 0.0456
• 20SMA: ₹1,200.00
• 50SMA: ₹1,180.00

✅ Signals:
• Golden Cross: 20 SMA > 50 SMA
• RSI Oversold (25.30)

✅ HDFC Bank (HDFCBANK.NS)
💰 Price: ₹1,567.89 | 📊 Score: 65/100
🎯 MODERATE BUY

📈 Indicators:
• RSI: 35.20
• MACD: 0.0234
• 20SMA: ₹1,550.00
• 50SMA: ₹1,540.00

✅ Signals:
• MACD crossed above signal

==================================================

⚠️ This is technical analysis only. Always do your own research before investing.
📊 Report generated at 1:00 PM IST daily during trading days.
```

### 🚨 Real-time Alerts (Score ≥ 50):
```
🎯 STOCK ALERT: Sunpharma

📊 Signal Score: 85/100
💰 Current Price: ₹1,234.56
📅 Date: 2024-01-15

🎯 Recommendation: STRONG BUY

📈 Key Indicators:
• RSI: 25.30
• MACD: 0.0456
• 20-day SMA: ₹1,200.00
• 50-day SMA: ₹1,180.00

✅ Active Signals:
• Golden Cross: 20 SMA > 50 SMA
• RSI Oversold (25.30)

⚠️ This is technical analysis only. Do your own research.
```

## ⏰ Alert Schedule

### 📅 Daily Report:
- **Time**: 1:00 PM IST daily
- **Days**: Monday to Friday (trading days only)
- **Content**: Comprehensive analysis of all stocks
- **Format**: Market summary + individual stock details

### 🚨 Real-time Alerts:
- **Trigger**: When any stock gets signal score ≥ 50
- **Frequency**: As soon as signals are detected
- **Content**: Individual stock alerts with key indicators

## 🔧 Customization

### Change Daily Report Time:
Edit line in `monitor_stock_mf.py`:
```python
schedule.every().day.at("13:00").do(run_daily_report, telegram_bot, symbols)
# Change "13:00" to your preferred time (24-hour format)
```

### Change Alert Threshold:
Edit line in `monitor_stock_mf.py`:
```python
if result['score'] >= 50:  # Change this number
```

### Add More Stocks:
Edit the `symbols` dictionary in the `main()` function.

### Customize Message Format:
Modify the `send_daily_report()` and `send_stock_alert()` methods in the `TelegramBot` class.

## 🛠️ Troubleshooting

### Bot Not Sending Messages:
1. Check if bot token is correct
2. Verify chat ID is correct
3. Make sure you've started a chat with your bot
4. Check Railway logs for error messages

### No Daily Report:
1. Verify it's a trading day (Monday-Friday)
2. Check if time is 1:00 PM IST
3. Look at Railway logs for any errors
4. Ensure environment variables are set correctly

### No Real-time Alerts:
1. Verify stocks have signal scores ≥ 50
2. Check if environment variables are set correctly
3. Look at Railway logs for any errors

### Bot Token Security:
- Never share your bot token publicly
- Use environment variables (not hardcoded in code)
- Railway securely stores environment variables

## 📊 Features Summary

✅ **Daily Report**: Comprehensive analysis at 1 PM IST  
✅ **Real-time Alerts**: Instant notifications for strong signals  
✅ **Trading Days Only**: Respects market holidays and weekends  
✅ **Rich Formatting**: Beautiful HTML messages with emojis  
✅ **Market Summary**: Overview of all stocks at a glance  
✅ **Individual Analysis**: Detailed breakdown for each stock  

---

**Ready to get daily stock reports and real-time alerts on Telegram?** Follow these steps and you'll never miss important market opportunities! 📈
