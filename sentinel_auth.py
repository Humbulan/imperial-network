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
