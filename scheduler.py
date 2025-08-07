import schedule
import time
import pytz
from datetime import datetime, timedelta
from stock_analyzer import LongTermStockMonitor
from config import (
    DAILY_REPORT_TIME, TIMEZONE, ALERT_THRESHOLD,
    TRADING_START_HOUR, TRADING_START_MINUTE,
    TRADING_END_HOUR, TRADING_END_MINUTE
)


def is_trading_day():
    """Check if current time is during Indian stock market trading days"""
    ist = pytz.timezone(TIMEZONE)
    now = datetime.now(ist)
    
    # Check if it's a weekday (Monday = 0, Sunday = 6)
    return now.weekday() < 5  # Monday to Friday


def is_trading_hours():
    """Check if current time is during Indian stock market trading hours"""
    ist = pytz.timezone(TIMEZONE)
    now = datetime.now(ist)
    
    # Check if it's a weekday
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    # Trading hours: 9:15 AM to 3:30 PM IST (configurable)
    start_time = now.replace(hour=TRADING_START_HOUR, minute=TRADING_START_MINUTE, second=0, microsecond=0)
    end_time = now.replace(hour=TRADING_END_HOUR, minute=TRADING_END_MINUTE, second=0, microsecond=0)
    
    return start_time <= now <= end_time


def get_next_trading_time():
    """Get the next time when trading will be active"""
    ist = pytz.timezone(TIMEZONE)
    now = datetime.now(ist)
    
    # If it's weekend, next trading time is Monday 9:15 AM
    if now.weekday() >= 5:  # Saturday or Sunday
        days_until_monday = (7 - now.weekday()) % 7
        next_monday = now + timedelta(days=days_until_monday)
        return next_monday.replace(hour=TRADING_START_HOUR, minute=TRADING_START_MINUTE, second=0, microsecond=0)
    
    # If it's before trading hours today
    if now.hour < TRADING_START_HOUR or (now.hour == TRADING_START_HOUR and now.minute < TRADING_START_MINUTE):
        return now.replace(hour=TRADING_START_HOUR, minute=TRADING_START_MINUTE, second=0, microsecond=0)
    
    # If it's after trading hours today, next trading time is tomorrow 9:15 AM
    if now.hour > TRADING_END_HOUR or (now.hour == TRADING_END_HOUR and now.minute > TRADING_END_MINUTE):
        tomorrow = now + timedelta(days=1)
        if tomorrow.weekday() < 5:  # If tomorrow is a weekday
            return tomorrow.replace(hour=TRADING_START_HOUR, minute=TRADING_START_MINUTE, second=0, microsecond=0)
        else:  # If tomorrow is weekend, next Monday
            days_until_monday = (7 - tomorrow.weekday()) % 7
            next_monday = tomorrow + timedelta(days=days_until_monday)
            return next_monday.replace(hour=TRADING_START_HOUR, minute=TRADING_START_MINUTE, second=0, microsecond=0)
    
    return None  # Currently in trading hours


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
    """Run continuous monitoring with smart scheduling and sleep during off-hours"""
    # Schedule daily report at configured time
    schedule.every().day.at(DAILY_REPORT_TIME).do(run_daily_report, telegram_bot, symbols)
    
    print(f"📅 Daily report scheduled for {DAILY_REPORT_TIME} IST (trading days only)")
    print(f"⏰ Trading hours: {TRADING_START_HOUR:02d}:{TRADING_START_MINUTE:02d} - {TRADING_END_HOUR:02d}:{TRADING_END_MINUTE:02d} IST (Mon-Fri)")
    print("🔄 Starting smart monitoring with trading hours detection...")

    # Keep the script running
    while True:
        try:
            # Check if we're in trading hours
            if is_trading_hours():
                print("📈 Trading hours active - monitoring stocks...")
                schedule.run_pending()
                time.sleep(60)  # Check every minute during trading hours
            else:
                # Outside trading hours - sleep until next trading time
                next_trading = get_next_trading_time()
                if next_trading:
                    ist = pytz.timezone(TIMEZONE)
                    now = datetime.now(ist)
                    sleep_seconds = (next_trading - now).total_seconds()
                    
                    if sleep_seconds > 0:
                        print(f"😴 Outside trading hours. Sleeping until {next_trading.strftime('%Y-%m-%d %H:%M IST')}")
                        print(f"⏰ Sleeping for {sleep_seconds/3600:.1f} hours...")
                        time.sleep(sleep_seconds)
                    else:
                        time.sleep(300)  # 5 minutes if calculation error
                else:
                    # Currently in trading hours but calculation failed
                    schedule.run_pending()
                    time.sleep(60)
                    
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
