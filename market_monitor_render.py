#!/usr/bin/env python3
"""
Indian Market Monitor for Render
Continuous running with health check endpoint
"""

import requests
import time
import json
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify

app = Flask(__name__)

class MarketMonitor:
    def __init__(self, telegram_bot_token, telegram_chat_id):
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.last_check = None
        self.last_alert = None
        
    def get_nifty_sensex_data(self):
        """Get current Nifty 50 and Sensex data"""
        try:
            # Using Yahoo Finance API for real-time data
            nifty_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
            sensex_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Get Nifty 50 data
            nifty_response = requests.get(nifty_url, headers=headers, timeout=10)
            nifty_data = nifty_response.json()
            
            # Get Sensex data
            sensex_response = requests.get(sensex_url, headers=headers, timeout=10)
            sensex_data = sensex_response.json()
            
            # Extract current and previous day data
            nifty_current = nifty_data['chart']['result'][0]['meta']['regularMarketPrice']
            nifty_previous = nifty_data['chart']['result'][0]['meta']['previousClose']
            
            sensex_current = sensex_data['chart']['result'][0]['meta']['regularMarketPrice']
            sensex_previous = sensex_data['chart']['result'][0]['meta']['previousClose']
            
            return {
                'nifty': {
                    'current': nifty_current,
                    'previous': nifty_previous,
                    'change': nifty_current - nifty_previous,
                    'change_percent': ((nifty_current - nifty_previous) / nifty_previous) * 100
                },
                'sensex': {
                    'current': sensex_current,
                    'previous': sensex_previous,
                    'change': sensex_current - sensex_previous,
                    'change_percent': ((sensex_current - sensex_previous) / sensex_previous) * 100
                }
            }
            
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None
    
    def check_market_conditions(self, data):
        """Check if market conditions indicate a downturn"""
        alerts = []
        
        # Check 1: Nifty 50 drops more than 2% in a day
        if data['nifty']['change_percent'] < -2:
            alerts.append(f"🚨 Nifty 50 down {data['nifty']['change_percent']:.2f}% (more than 2%)")
        
        # Check 2: Both Sensex and Nifty are in red
        if data['nifty']['change_percent'] < 0 and data['sensex']['change_percent'] < 0:
            alerts.append(f"📉 Both indices in red: Nifty {data['nifty']['change_percent']:.2f}%, Sensex {data['sensex']['change_percent']:.2f}%")
        
        # Check 3: Market opens gap down by more than 1%
        if data['nifty']['change_percent'] < -1:
            alerts.append(f"⚡ Market gap down: Nifty {data['nifty']['change_percent']:.2f}%")
        
        return alerts
    
    def send_telegram_alert(self, message):
        """Send alert via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Alert sent successfully!")
                self.last_alert = datetime.now()
                return True
            else:
                print(f"❌ Failed to send alert: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")
            return False
    
    def create_alert_message(self, data, alerts):
        """Create formatted alert message"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"<b>🇮🇳 Indian Market Alert</b>\n"
        message += f"⏰ {current_time}\n\n"
        
        message += f"<b>Market Status:</b>\n"
        message += f"Nifty 50: {data['nifty']['current']:.2f} ({data['nifty']['change_percent']:+.2f}%)\n"
        message += f"Sensex: {data['sensex']['current']:.2f} ({data['sensex']['change_percent']:+.2f}%)\n\n"
        
        message += f"<b>🚨 Alerts:</b>\n"
        for alert in alerts:
            message += f"• {alert}\n"
        
        message += f"\n<b>Overall Market Sentiment:</b> {'🔴 BEARISH' if len(alerts) > 0 else '🟢 NORMAL'}"
        message += f"\n\n<i>Alert from Render Market Monitor</i>"
        
        return message
    
    def is_market_open(self):
        """Check if Indian market is open (9:15 AM - 3:30 PM IST)"""
        from datetime import datetime
        import pytz
        
        # Get current time in IST
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist)
        
        # Check if it's a weekday (Monday = 0, Sunday = 6)
        if current_time.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Check if it's within market hours (9:15 AM - 3:30 PM IST)
        market_start = current_time.replace(hour=9, minute=15, second=0, microsecond=0)
        market_end = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_start <= current_time <= market_end
    
    def check_market_once(self):
        """Check market once and send alert if needed"""
        if not self.is_market_open():
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Market closed")
            return
        
        # Get current market data
        data = self.get_nifty_sensex_data()
        
        if not data:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to fetch market data")
            return
        
        # Update last check time
        self.last_check = datetime.now()
        
        # Print current status
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Nifty: {data['nifty']['current']:.2f} ({data['nifty']['change_percent']:+.2f}%) | Sensex: {data['sensex']['current']:.2f} ({data['sensex']['change_percent']:+.2f}%)")
        
        # Check for alert conditions
        alerts = self.check_market_conditions(data)
        
        if alerts:
            print(f"🚨 {len(alerts)} alert(s) triggered!")
            message = self.create_alert_message(data, alerts)
            self.send_telegram_alert(message)
        else:
            print("✅ Market conditions normal")

# Global monitor instance
monitor = None

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    global monitor
    
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'last_check': monitor.last_check.isoformat() if monitor and monitor.last_check else None,
        'last_alert': monitor.last_alert.isoformat() if monitor and monitor.last_alert else None,
        'market_open': monitor.is_market_open() if monitor else False
    }
    
    return jsonify(status)

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>🇮🇳 Indian Market Monitor</h1>
    <p>Running on Render</p>
    <p><a href="/health">Health Check</a></p>
    """

def start_monitor():
    """Start the monitoring loop in background"""
    global monitor
    
    while True:
        try:
            monitor.check_market_once()
            time.sleep(300)  # Wait 5 minutes
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    # Get credentials from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Missing Telegram credentials in environment variables")
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in Render")
        exit(1)
    
    print("✅ Telegram credentials loaded from environment")
    
    # Create monitor instance
    monitor = MarketMonitor(bot_token, chat_id)
    
    # Start monitoring in background thread
    import threading
    monitor_thread = threading.Thread(target=start_monitor, daemon=True)
    monitor_thread.start()
    
    print("🚀 Starting Render Market Monitor...")
    print("📊 Monitoring every 5 minutes during market hours")
    print("🌐 Health check available at /health")
    
    # Start Flask app
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
