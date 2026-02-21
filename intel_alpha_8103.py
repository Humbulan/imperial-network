#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from datetime import datetime

class IntelAlphaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Market intelligence data
        commodities = [
            {'name': 'Maize', 'price': 250.50, 'trend': 'up', 'volume': 1250},
            {'name': 'Tomatoes', 'price': 204.31, 'trend': 'stable', 'volume': 850},
            {'name': 'Chickens', 'price': 465.42, 'trend': 'up', 'volume': 320},
            {'name': 'Eggs', 'price': 51.96, 'trend': 'down', 'volume': 1500},
            {'name': 'Wood Carvings', 'price': 425.15, 'trend': 'up', 'volume': 75}
        ]
        
        response = {
            'service': 'Intel_Alpha',
            'status': 'online',
            'market_intelligence': commodities,
            'farmer_activity': {
                'active_farmers': 87,
                'new_listings_today': 12,
                'avg_transaction': 325.75
            },
            'predictions': {
                'next_week_sentiment': 'bullish',
                'expected_growth': 8.5,
                'confidence': 0.87
            },
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

print("🧠 Intel Alpha starting on port 8103...")
HTTPServer(('0.0.0.0', 8103), IntelAlphaHandler).serve_forever()
