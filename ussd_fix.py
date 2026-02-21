from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class USSDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'USSD_Portal',
            'status': 'online',
            'message': 'USSD GATEWAY ACTIVE',
            'endpoints': ['/ussd', '/ussd/simulate', '/ussd/admin'],
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Simple USSD response
        response = "CON Welcome to Imperial USSD\n1. Check Balance\n2. Make Payment\n3. Exit"
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args): 
        return

print("🚀 Starting USSD Portal on port 8087...")
HTTPServer(('0.0.0.0', 8087), USSDHandler).serve_forever()
