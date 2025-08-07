import schedule
import time
import pytz
from datetime import datetime
from stock_analyzer import LongTermStockMonitor
from config import DAILY_REPORT_TIME, TIMEZONE, ALERT_THRESHOLD


def is_trading_day():
    """Check if current time is during Indian stock market trading days"""
    ist = pytz.timezone(TIMEZONE)
    now = datetime.now(ist)
    
    # Check if it's a weekday (Monday = 0, Sunday = 6)
    return now.weekday() < 5  # Monday to Friday


def run_daily_report(telegram_bot, symbols):
    """Run daily report at 1 PM IST"""
    if not is_trading_day():
        print("Not a trading day. Skipping daily report.")
        return
    
    print("📊 Generating daily stock market report...")
    
    all_results = []
    
    for symbol, name in symbols.items():
        print(f"Analyzing {name}...")
        monitor = LongTermStockMonitor(symbol)
        result = monitor.analyze()
        if result:
            result['name'] = name  # Add name for display
            all_results.append(result)
    
    if telegram_bot and all_results:
        telegram_bot.send_daily_report(all_results)
        print("✅ Daily report sent to Telegram")
    else:
        print("❌ Failed to generate daily report")


def run_continuous_monitoring(telegram_bot, symbols):
    """Run continuous monitoring with scheduling"""
    # Schedule daily report at configured time
    schedule.every().day.at(DAILY_REPORT_TIME).do(run_daily_report, telegram_bot, symbols)
    
    print(f"📅 Daily report scheduled for {DAILY_REPORT_TIME} IST (trading days only)")
    print("🔄 Starting continuous monitoring...")

    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("Service stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(300)  # Wait 5 minutes before retrying


def run_single_analysis(symbols, telegram_bot=None):
    """Run single analysis of all stocks"""
    print("\n📊 MULTI-STOCK LONG-TERM TECHNICAL MONITOR")
    print("=" * 70)

    for symbol, name in symbols.items():
        print(f"\n{'='*70}")
        print(f"🔍 {name.upper()} ANALYSIS ({symbol})")
        print(f"{'='*70}")
        
        monitor = LongTermStockMonitor(symbol)
        result = monitor.analyze()
        
        if not result:
            print("⚠️ Data unavailable.")
            continue

        # Print analysis to console
        from stock_analyzer import print_stock_analysis
        print_stock_analysis(result, name)

        # Send Telegram alert for strong signals
        if telegram_bot and result['score'] >= ALERT_THRESHOLD:
            telegram_bot.send_stock_alert(result, name)

    print(f"\n{'='*70}")
    print("📌 Note: This is a long-term technical perspective. Use with fundamental analysis.")
    print("📘 Signal Score Legend:")
    print("   • 70–100: Strong Buy")
    print("   • 50–69 : Moderate Buy")
    print("   • 30–49 : Weak Buy")
    print("   • 0–29  : Hold / Avoid")
    print("=" * 70)
