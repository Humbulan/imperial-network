#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class IntelAlphaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/wealth/settlement':
            self.handle_settlement()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "service": "Intel_Alpha",
                "status": "online",
                "timestamp": str(datetime.now())
            }
            self.wfile.write(json.dumps(response).encode())

    def handle_settlement(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        try:
            with open('wealth_lock.json', 'r') as f:
                data = json.load(f)
            
            portfolio = 11345774.22
            # Use the R238M Market Gain for collateral
            market_gain = data.get('market_gain', 238050000.00)
            collateral = market_gain * 0.7
            
            response = {
                "status": "ready",
                "portfolio": portfolio,
                "wealth_lock_collateral": collateral,
                "total_buying_power": portfolio + collateral,
                "mtn_shares_secured": 883321,
                "projected_dividend": 353328.40,
                "timestamp": str(datetime.now())
            }
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        return

print("🧠 Intel Alpha (Fixed) starting on port 8103...")
HTTPServer(('0.0.0.0', 8103), IntelAlphaHandler).serve_forever()
