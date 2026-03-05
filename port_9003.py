#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class SurveyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "service": "Crop Monitoring",
            "port": 9003,
            "status": "online",
            "timestamp": str(datetime.now())
        }
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        return

print("📋 Crop Monitoring starting on port 9003...")
HTTPServer(('0.0.0.0', 9003), SurveyHandler).serve_forever()
