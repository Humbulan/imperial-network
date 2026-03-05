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
            "service": "Malamulele Pipe Repair",
            "port": 9002,
            "status": "online",
            "timestamp": str(datetime.now())
        }
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        return

print("📋 Malamulele Pipe Repair starting on port 9002...")
HTTPServer(('0.0.0.0', 9002), SurveyHandler).serve_forever()
