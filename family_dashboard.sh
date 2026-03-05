#!/bin/bash
# 🏠 Family Dashboard - Quick overview

cd ~/imperial_network
clear
echo "🏠 IMPERIAL FAMILY DASHBOARD"
echo "="*50
python3 milestone_alert.py | grep -E "Total Available|Milestones|Next|Daily Family|Monthly Family|School Fees"
echo "="*50
echo "📁 Last 5 dividend entries:"
tail -5 ~/imperial_vault/family_dividends.log 2>/dev/null || echo "No entries yet"
