#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class IntelFilesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Get list of intelligence files
        files = []
        if os.path.exists('intel'):
            files = os.listdir('intel')
        
        response = {
            'service': 'Intel_Files',
            'status': 'online',
            'classification': 'TOP SECRET',
            'files': files[:10],
            'total_files': len(files),
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

print("📁 Intel Files starting on port 8191...")
HTTPServer(('0.0.0.0', 8191), IntelFilesHandler).serve_forever()
