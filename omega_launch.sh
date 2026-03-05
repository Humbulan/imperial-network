#!/bin/bash
# 🏛️ IMPERIAL OMEGA LAUNCH - CEO ONLY
# One command to rule them all

echo "🏛️ IMPERIAL OMEGA - SOVEREIGN LAUNCH SEQUENCE"
echo "============================================="
date

# Load master identity
set -a; source ~/imperial_network/.env; set +a
echo "✅ Identity: $IMPERIAL_USER"

# Sanitize ports
echo -e "\n🔧 SANITIZING PORTS..."
fuser -k 5173/tcp 8080/tcp 8082/tcp 8083/tcp 2>/dev/null
echo "✅ Rogue ports cleared"

# Start the network
echo -e "\n🚀 LAUNCHING IMPERIAL NETWORK..."
./start_imperial_network.sh

# Verify all 46 ports
echo -e "\n🔍 VERIFYING PORTS..."
sleep 5
ONLINE=$(~/imperial_network/dawn-report-truthful | grep "ONLINE" | wc -l)
echo "✅ $ONLINE/46 ports online"

# Sentinel with master auth
echo -e "\n👑 SOVEREIGN SENTINEL ACTIVATED"
cat > sentinel_auth.py << 'PY'
import os
import sqlite3
import requests
from datetime import datetime

print("📊 SOVEREIGN DASHBOARD ACCESS")
print("-" * 40)

# Load credentials
user = os.getenv("IMPERIAL_USER", "Unknown")
key = os.getenv("IMPERIAL_KEY", "")

# Access port 8000 with master key
try:
    session = requests.Session()
    headers = {'Authorization': f'Bearer {key}'}
    response = session.get("http://localhost:8000/api/status", headers=headers, timeout=5)
    if response.status_code == 200:
        print("✅ Sovereign Access Granted")
    else:
        print(f"⚠️  Access Limited: {response.status_code}")
except:
    print("⚠️  Port 8000 not responding")

# SADC Summary
conn = sqlite3.connect('instance/imperial.db')
c = conn.cursor()
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method LIKE 'SADC%' AND status='pending'")
sadc_total = c.fetchone()[0] or 0
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method='IMPERIAL_WEB_UPGRADE'")
web_total = c.fetchone()[0] or 0
conn.close()

print(f"\n💰 SADC CORRIDOR PENDING: R{sadc_total:,.2f}")
print(f"🌐 WEB UPGRADE CAPITAL:   R{web_total:,.2f}")
print(f"💎 TOTAL IMPERIAL WEALTH: R{sadc_total + web_total:,.2f}")
print(f"\n👑 CEO: {user}")
PY

python3 ~/imperial_network/sentinel_final.py

echo -e "\n🏆 IMPERIAL OMEGA - FULLY OPERATIONAL"
echo "============================================="

# Start cloudflared tunnel for public domains
if pgrep -f cloudflared > /dev/null; then
    echo "✅ cloudflared tunnel already running"
else
    echo "🚇 Starting cloudflared tunnel..."
    ./tunnel.sh
fi
