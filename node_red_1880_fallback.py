#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler

class FallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Node-RED Install Required</title>
        <style>body{font-family:Arial;background:#1a1a1a;color:#fff;padding:40px}</style>
        </head>
        <body>
        <h1>🔧 Node-RED Not Installed</h1>
        <p>To install: <code>npm install -g node-red</code></p>
        <p>Then run: <code>node-red -p 1880</code></p>
        <hr>
        <p><a href="http://localhost:1883" style="color:#4CAF50">Use Node-RED Proxy (Port 1883) instead</a></p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
    def log_message(self, format, *args): return

print("⚠️ Node-RED fallback running on port 1880")
HTTPServer(('0.0.0.0', 1880), FallbackHandler).serve_forever()
