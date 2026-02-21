from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class MalamuleleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'Malamulele_Portal',
            'status': 'online',
            'region': 'Limpopo',
            'villages': ['Malamulele Plaza', 'Masingita Crossing', 'Matsila', 'Altein', 'Ka-Mahonisi'],
            'active_users': 157,
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args): 
        return

print("🚀 Starting Malamulele Portal on port 8100...")
HTTPServer(('0.0.0.0', 8100), MalamuleleHandler).serve_forever()
