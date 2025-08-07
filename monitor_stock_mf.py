#!/usr/bin/env python3
"""
Stock Market Monitor - Main Application
A modular stock monitoring system with Telegram alerts and daily reports.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import initialize_telegram_bot
from scheduler import run_continuous_monitoring, run_single_analysis
from config import STOCK_SYMBOLS


def main():
    """Main application entry point"""
    print("🚀 Starting Stock Market Monitor...")
    
    # Initialize Telegram bot
    telegram_bot = initialize_telegram_bot()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Run single analysis
        print("📊 Running single analysis...")
        run_single_analysis(STOCK_SYMBOLS, telegram_bot)
    else:
        # Run continuous monitoring
        print("🔄 Starting continuous monitoring...")
        run_continuous_monitoring(telegram_bot, STOCK_SYMBOLS)


if __name__ == "__main__":
    main()
