#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class SADCHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'service': 'SADC_Sync',
            'status': 'online',
            'corridor': 'Zim/Moz',
            'countries': ['Zimbabwe', 'Mozambique', 'South Africa'],
            'active': True,
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

def run_server():
    server = HTTPServer(('0.0.0.0', 8112), SADCHandler)
    print("🌍 SADC Sync running on port 8112")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
