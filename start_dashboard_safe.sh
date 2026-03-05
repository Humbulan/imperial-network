#!/bin/bash
# 🏛️ Safe Dashboard Starter - Handles database locks gracefully

cd ~/imperial_network

# Kill any existing dashboard
pkill -f dashboard_ui_fixed.py
sleep 2

# Start with retry logic in a wrapper
while true; do
    echo "🚀 Starting Imperial Dashboard (PID: $$)..."
    python3 dashboard_ui_fixed.py
    echo "⚠️ Dashboard crashed, restarting in 5 seconds..."
    sleep 5
done
