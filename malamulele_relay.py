from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class RelayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'Malamulele_Relay',
            'status': 'online',
            'relay_to': ['Thohoyandou (8110)', 'SADC_Sync (8112)', 'Urban_Gateway (8102)'],
            'messages_relayed': 1247,
            'uptime': '99.8%',
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args): 
        return

print("🔄 Starting Malamulele Relay on port 8111...")
HTTPServer(('0.0.0.0', 8111), RelayHandler).serve_forever()
