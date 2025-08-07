import requests
import os
from datetime import datetime
import pytz
from config import ALERT_THRESHOLD, TIMEZONE


class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message):
        """Send message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Telegram alert sent successfully")
            else:
                print(f"❌ Failed to send Telegram alert: {response.text}")
        except Exception as e:
            print(f"❌ Error sending Telegram alert: {e}")
    
    def send_stock_alert(self, result, name):
        """Send formatted stock alert"""
        if result['score'] >= ALERT_THRESHOLD:  # Send alerts for configured threshold and above
            from config import STRONG_BUY_THRESHOLD
            emoji = "🎯" if result['score'] >= STRONG_BUY_THRESHOLD else "✅"
            recommendation = "STRONG BUY" if result['score'] >= STRONG_BUY_THRESHOLD else "MODERATE BUY"
            
            message = f"""
{emoji} <b>STOCK ALERT: {name}</b>

📊 <b>Signal Score:</b> {result['score']}/100
💰 <b>Current Price:</b> ₹{result['price']:.2f}
📅 <b>Date:</b> {result['date']}

🎯 <b>Recommendation:</b> {recommendation}

📈 <b>Key Indicators:</b>
• RSI: {result['rsi']:.2f}
• MACD: {result['macd']:.4f}
• 20-day SMA: ₹{result['sma_20']:.2f}
• 50-day SMA: ₹{result['sma_50']:.2f}

✅ <b>Active Signals:</b>
"""
            
            if result['signals']:
                for desc in result['signals'].values():
                    message += f"• {desc}\n"
            else:
                message += "• No active signals\n"
            
            message += f"\n⚠️ <i>This is technical analysis only. Do your own research.</i>"
            
            self.send_message(message)
    
    def send_daily_report(self, all_results):
        """Send daily comprehensive report of all stocks"""
        if not all_results:
            return
        
        # Sort results by signal score (highest first)
        sorted_results = sorted(all_results, key=lambda x: x['score'], reverse=True)
        
        message = f"""
📊 <b>DAILY STOCK MARKET REPORT</b>
📅 <b>Date:</b> {datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M IST')}

{'='*50}

"""
        
        # Summary section
        from config import STRONG_BUY_THRESHOLD, MODERATE_BUY_THRESHOLD, WEAK_BUY_THRESHOLD
        strong_buy_count = sum(1 for r in all_results if r['score'] >= STRONG_BUY_THRESHOLD)
        moderate_buy_count = sum(1 for r in all_results if MODERATE_BUY_THRESHOLD <= r['score'] < STRONG_BUY_THRESHOLD)
        weak_buy_count = sum(1 for r in all_results if WEAK_BUY_THRESHOLD <= r['score'] < MODERATE_BUY_THRESHOLD)
        hold_count = sum(1 for r in all_results if r['score'] < WEAK_BUY_THRESHOLD)
        
        message += f"""
📈 <b>MARKET SUMMARY:</b>
🎯 Strong Buy: {strong_buy_count} stocks
✅ Moderate Buy: {moderate_buy_count} stocks  
💡 Weak Buy: {weak_buy_count} stocks
❌ Hold: {hold_count} stocks

{'='*50}

"""
        
        # Individual stock analysis
        for result in sorted_results:
            name = result.get('name', result['symbol'])
            emoji = "🎯" if result['score'] >= STRONG_BUY_THRESHOLD else "✅" if result['score'] >= MODERATE_BUY_THRESHOLD else "💡" if result['score'] >= WEAK_BUY_THRESHOLD else "❌"
            recommendation = "STRONG BUY" if result['score'] >= STRONG_BUY_THRESHOLD else "MODERATE BUY" if result['score'] >= MODERATE_BUY_THRESHOLD else "WEAK BUY" if result['score'] >= WEAK_BUY_THRESHOLD else "HOLD"
            
            message += f"""
{emoji} <b>{name}</b> ({result['symbol']})
💰 Price: ₹{result['price']:.2f} | 📊 Score: {result['score']}/100
🎯 <b>{recommendation}</b>

📈 <b>Indicators:</b>
• RSI: {result['rsi']:.2f}
• MACD: {result['macd']:.4f}
• 20SMA: ₹{result['sma_20']:.2f}
• 50SMA: ₹{result['sma_50']:.2f}

"""
            
            if result['signals']:
                message += "✅ <b>Signals:</b>\n"
                for desc in result['signals'].values():
                    message += f"• {desc}\n"
            else:
                message += "• No active signals\n"
            
            message += "\n"
        
        message += f"""
{'='*50}

⚠️ <i>This is technical analysis only. Always do your own research before investing.</i>
📊 <i>Report generated at 1:00 PM IST daily during trading days.</i>
"""
        
        self.send_message(message)


def initialize_telegram_bot():
    """Initialize Telegram bot from environment variables"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if bot_token and chat_id:
        telegram_bot = TelegramBot(bot_token, chat_id)
        print("✅ Telegram bot initialized")
        return telegram_bot
    else:
        print("⚠️ Telegram bot not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        return None
