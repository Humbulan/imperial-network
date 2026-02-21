from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'Dashboard_UI',
            'status': 'online',
            'version': '2.0.0',
            'features': ['System Monitor', 'Village Management', 'API Keys', 'AI Analytics'],
            'endpoints': ['/dashboard', '/admin/villages', '/ai/dashboard', '/monitor'],
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args): 
        return

print("🖥️ Starting Dashboard UI on port 8092...")
HTTPServer(('0.0.0.0', 8092), DashboardHandler).serve_forever()
