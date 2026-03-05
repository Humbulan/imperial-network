#!/usr/bin/env python3
"""
Temperature Logger - Logs A73 temperature to file and alerts if >40°C
"""
import requests
import time
import json
import os
from datetime import datetime

LOG_FILE = "logs/temperature.log"
ALERT_FILE = "logs/temperature_alerts.log"
STATS_URL = "http://localhost:8093"

def log_message(msg, is_alert=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {msg}\n"
    
    # Always log to main log
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    # Also log alerts to separate file
    if is_alert:
        with open(ALERT_FILE, "a") as f:
            f.write(log_entry)
        print(f"🔴 ALERT: {msg}")
    else:
        print(f"ℹ️ {msg}")

def check_temperature():
    try:
        response = requests.get(STATS_URL, timeout=5)
        data = response.json()
        
        battery = data.get('battery', {})
        temp = battery.get('temp')
        level = battery.get('level')
        status = battery.get('status')
        
        # Convert temperature if needed (some Android returns in tenths)
        if temp and temp > 100:
            temp = temp / 10
        
        device = data.get('device', {})
        model = device.get('model', 'SM-A736B')
        
        temp_c = float(temp) if temp else 0
        
        # Check thresholds
        if temp_c > 45:
            log_message(f"🔥 CRITICAL: Temperature at {temp_c}°C on {model}! Battery: {level}% - SHUTDOWN RISK!", True)
        elif temp_c > 40:
            log_message(f"⚠️ WARNING: Temperature at {temp_c}°C on {model}. Battery: {level}% - Consider cooling", True)
        elif temp_c > 35:
            log_message(f"ℹ️ Elevated temperature: {temp_c}°C on {model}. Battery: {level}%")
        else:
            log_message(f"✅ Normal: {temp_c}°C on {model}. Battery: {level}%")
        
        return temp_c
        
    except Exception as e:
        log_message(f"❌ Error checking temperature: {e}", True)
        return None

def main():
    print("🌡️ A73 Temperature Monitor Started")
    print("===================================")
    
    # Create logs directory if needed
    os.makedirs("logs", exist_ok=True)
    
    # Check immediately
    check_temperature()
    
    # Then check every 60 seconds
    try:
        while True:
            time.sleep(60)
            check_temperature()
    except KeyboardInterrupt:
        print("\n👋 Temperature monitor stopped")

if __name__ == "__main__":
    main()
