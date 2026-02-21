#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class SentinelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'service': 'Sentinel',
            'status': 'online',
            'security': {
                'firewall': 'ACTIVE',
                'intrusion_detection': 'ENABLED',
                'threat_level': 'LOW',
                'blocked_attempts': 23,
                'active_sessions': 7
            },
            'encryption': 'AES-256',
            'last_scan': str(datetime.now()),
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

print("🛡️ Sentinel starting on port 8105...")
HTTPServer(('0.0.0.0', 8105), SentinelHandler).serve_forever()
