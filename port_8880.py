#!/usr/bin/env python3
"""
🚇 HA TUNNEL - Stabilized Version
Handles Cloudflare HEAD health checks silently
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class HATunnelHandler(BaseHTTPRequestHandler):
    # This silences the 501 error by accepting Cloudflare's health check
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # No body for HEAD requests

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'HA_TUNNEL',
            'description': 'Secure Communication Tunnel',
            'status': 'online',
            'port': 8880,
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    print("🚇 HA TUNNEL stabilizer active on port 8880")
    print("   ✅ HEAD requests handled - No more 501 errors")
    HTTPServer(('0.0.0.0', 8880), HATunnelHandler).serve_forever()
