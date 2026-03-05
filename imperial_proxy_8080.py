#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json

class ImperialProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Route to appropriate backend
        if self.path.startswith('/api/'):
            # API requests go to port 8000
            backend = '8000'
        elif self.path == '/' or self.path.startswith('/static/'):
            # Frontend requests go to port 8088
            backend = '8088'
        elif self.path.startswith('/dashboard'):
            # Dashboard goes to 8092
            backend = '8092'
        elif self.path.startswith('/monitor'):
            # Monitor goes to 8090
            backend = '8090'
        elif self.path.startswith('/ai'):
            # AI dashboard goes to 8000
            backend = '8000'
        else:
            # Default to frontend
            backend = '8088'
        
        try:
            # Proxy the request
            url = f'http://localhost:{backend}{self.path}'
            req = urllib.request.Request(url, headers=dict(self.headers))
            
            with urllib.request.urlopen(req, timeout=5) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Bad Gateway', 'message': str(e)}).encode())
    
    def do_POST(self):
        # All POST requests go to API
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            req = urllib.request.Request(
                f'http://localhost:8000{self.path}',
                data=post_data,
                headers=dict(self.headers),
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        return

print("🌐 Imperial Proxy starting on port 8080...")
print("📡 Unified entry point: http://localhost:8080")
HTTPServer(('0.0.0.0', 8080), ImperialProxyHandler).serve_forever()
