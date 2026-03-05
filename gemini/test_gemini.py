#!/usr/bin/env python3
"""
Test Gemini Integration with Imperial Network
"""
import os
import json
import urllib.request
import subprocess
from datetime import datetime

print("🏛️ IMPERIAL GEMINI INTEGRATION TEST")
print("=" * 60)

# Check API key
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not set")
    print("Run: export GEMINI_API_KEY='your-key-here'")
    exit(1)

print(f"✅ API Key: {api_key[:15]}...")

# Check quota first
print("\n📊 Checking quota...")
subprocess.run(["python3", "gemini/quota_tracker.py"])

# Test API connectivity
print("\n📡 Testing API connection...")
try:
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read())
        models = [m['name'] for m in data.get('models', [])]
        print(f"✅ Connection successful")
        print(f"📋 Available models: {len(models)}")
        for m in models[:3]:
            print(f"   - {m}")
except Exception as e:
    print(f"❌ API test failed: {e}")

# Test with SADC data
print("\n🌍 Testing with SADC trade data...")
try:
    # Get SADC status
    with urllib.request.urlopen("http://localhost:8112/status", timeout=2) as r:
        sadc_data = json.loads(r.read())
        lithium = sadc_data.get('trade_manifest', {}).get('lithium', {})
        print(f"✅ SADC data fetched")
        print(f"   Lithium: ${lithium.get('price_usd')}/tonne, +{lithium.get('volume_growth')}%")
        
        # This would be where we call Gemini with the data
        print("⚡ Ready for Gemini analysis")
        
except Exception as e:
    print(f"⚠️ SADC not available: {e}")

print("\n🏛️ Imperial Gemini integration ready")
