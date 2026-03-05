#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os
import re
from datetime import datetime

class SimpleStatsHandler(BaseHTTPRequestHandler):
    def get_ledger_total(self):
        total = 0.0
        log_path = '/data/data/com.termux/files/home/imperial_network/logs/contract_ledger.log'
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                for line in f:
                    match = re.search(r'Growth Split: R(\d+\.?\d*)', line)
                    if match:
                        total += float(match.group(1))
        return total

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        base_capital = 1550000.0  # The .31% foundation
        ledger_growth = self.get_ledger_total()
        total_growth = base_capital + ledger_growth
        target = 500000000.0
        progress = (total_growth / target) * 100

        stats = {
            'timestamp': datetime.now().isoformat(),
            'service': 'Imperial Network System Stats',
            'port': 8093,
            'status': 'online',
            'financials': {
                'base_capital_zar': base_capital,
                'ledger_growth_zar': ledger_growth,
                'total_allocated_zar': total_growth,
                'progress_to_r500m': f"{progress:.4f}%"
            },
            'infrastructure': {
                'pid': os.getpid(),
                'uptime': time.time()
            }
        }
        self.wfile.write(json.dumps(stats, indent=2).encode())

if __name__ == '__main__':
    print(f"🏛️  SOVEREIGN STATS UPGRADED ON PORT 8093")
    server = HTTPServer(('0.0.0.0', 8093), SimpleStatsHandler)
    server.allow_reuse_address = True
    server.serve_forever()
