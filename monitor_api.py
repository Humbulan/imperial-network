#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import os

API_URL = "http://localhost:8000"
LOG_FILE = "api_monitor.log"

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def check_endpoint(endpoint, expected_status=200):
    try:
        url = f"{API_URL}{endpoint}"
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = (time.time() - start_time) * 1000
        
        status = "✅" if response.status_code == expected_status else "❌"
        log_message(f"{status} {endpoint} - {response.status_code} ({response_time:.0f}ms)")
        
        return {
            'endpoint': endpoint,
            'status': response.status_code,
            'time': response_time,
            'success': response.status_code == expected_status
        }
    except Exception as e:
        log_message(f"❌ {endpoint} - ERROR: {str(e)}")
        return {'endpoint': endpoint, 'error': str(e), 'success': False}

def check_business_api():
    """Check business API with premium key"""
    try:
        url = f"{API_URL}/api/business/data"
        headers = {'Authorization': 'Bearer PREMIUM_KEY_A1B2C3D4'}
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=5)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            log_message(f"✅ /api/business/data (with key) - 200 ({response_time:.0f}ms)")
        else:
            log_message(f"❌ /api/business/data (with key) - {response.status_code}")
    except Exception as e:
        log_message(f"❌ /api/business/data (with key) - ERROR: {str(e)}")

def main():
    log_message("="*50)
    log_message("🚀 Starting API Monitor")
    log_message("="*50)
    
    endpoints = [
        '/api/health',
        '/api/version',
        '/api/system/status',
        '/api/mobile/config'
    ]
    
    results = []
    for endpoint in endpoints:
        results.append(check_endpoint(endpoint))
    
    check_business_api()
    
    # Summary
    success_count = sum(1 for r in results if r.get('success', False))
    log_message("="*50)
    log_message(f"📊 Summary: {success_count}/{len(endpoints)} endpoints healthy")
    log_message("="*50)
    
    return all(r.get('success', False) for r in results)

if __name__ == "__main__":
    main()
