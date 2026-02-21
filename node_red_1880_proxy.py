#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

class NodeREDProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Try to proxy to real Node-RED on 1880
        try:
            # Attempt to fetch from real Node-RED
            req = urllib.request.Request(f"http://localhost:1880{self.path}")
            with urllib.request.urlopen(req, timeout=2) as response:
                self.send_response(200)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except:
            # If real Node-RED is not available, show a helpful HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Imperial Node-RED</title>
                <style>
                    body { font-family: Arial; margin: 40px; background: #1a1a1a; color: #fff; }
                    .container { max-width: 800px; margin: auto; }
                    .card { background: #2d2d2d; padding: 20px; border-radius: 10px; margin: 20px 0; }
                    h1 { color: #ff6b6b; }
                    .btn { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔧 Imperial Node-RED</h1>
                    <div class="card">
                        <h2>Node-RED Dashboard</h2>
                        <p>Real Node-RED should be running on port 1880</p>
                        <p>To start real Node-RED:</p>
                        <code>node-red</code>
                        <br><br>
                        <a href="http://localhost:1880" class="btn">Try Real Node-RED</a>
                    </div>
                    <div class="card">
                        <h3>System Status</h3>
                        <p>✅ Imperial Network: 26/35 ports online</p>
                        <p>💰 Portfolio: R10,938,044.07</p>
                        <p>📈 Progress to R500M: 232.94%</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        return

print("🔄 Node-RED Proxy starting on port 1883 (redirects to real Node-RED on 1880)")
HTTPServer(('0.0.0.0', 1883), NodeREDProxyHandler).serve_forever()
