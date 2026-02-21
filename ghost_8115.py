#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class GhostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'service': 'Ghost',
            'status': 'online',
            'visibility': 'STEALTH',
            'encryption': 'AES-256-GCM',
            'traffic': {
                'obfuscated': True,
                'routing': 'TOR',
                'hops': 3
            },
            'message': '👻 This node does not exist',
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

print("👻 Ghost starting on port 8115...")
HTTPServer(('0.0.0.0', 8115), GhostHandler).serve_forever()
