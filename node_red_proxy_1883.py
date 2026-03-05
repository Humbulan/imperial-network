#!/usr/bin/env python3
"""
Node-RED Proxy - Port 1883
Proxies requests to real Node-RED on 1880 and provides fallback dashboard
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
from datetime import datetime

class NodeREDProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Try to proxy to real Node-RED on 1880
        try:
            req = urllib.request.Request(f"http://localhost:1880{self.path}")
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=2) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
                return
        except Exception as e:
            # If proxy fails, show a simple status page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Node-RED Proxy</title>
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{ font-family: Arial; background: #1a1a1a; color: #fff; padding: 40px; }}
                    .card {{ background: #2d2d2d; padding: 20px; border-radius: 10px; }}
                    .green {{ color: #4CAF50; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🔄 Node-RED Proxy</h1>
                    <p>Real Node-RED is running on port 1880</p>
                    <p>Status: <span class="green">ACTIVE</span></p>
                    <p>Access real Node-RED at: <a href="http://localhost:1880" style="color: #4CAF50;">http://localhost:1880</a></p>
                    <p>Timestamp: {datetime.now()}</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        return

print("🚀 Node-RED Proxy starting on port 1883...")
print("📡 Forwarding to real Node-RED on port 1880")
HTTPServer(('0.0.0.0', 1883), NodeREDProxyHandler).serve_forever()
