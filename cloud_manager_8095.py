#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime

class CloudManagerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get directory structure
            root_dir = os.path.abspath('.')
            files = []
            for item in os.listdir(root_dir):
                item_path = os.path.join(root_dir, item)
                files.append({
                    'name': item,
                    'type': 'directory' if os.path.isdir(item_path) else 'file',
                    'size': os.path.getsize(item_path) if os.path.isfile(item_path) else 0,
                    'modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                })
            
            response = {
                'service': 'Cloud_Manager',
                'status': 'online',
                'root_directory': root_dir,
                'files': files,
                'stats': {
                    'total_files': len([f for f in files if f['type'] == 'file']),
                    'total_directories': len([f for f in files if f['type'] == 'directory']),
                    'total_size': sum(f['size'] for f in files if f['type'] == 'file')
                },
                'timestamp': str(datetime.now())
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            # Serve files for other paths
            super().do_GET()
    
    def log_message(self, format, *args):
        return

print("☁️ Cloud Manager starting on port 8095...")
print("📁 Serving directory: ~/imperial_network/")
HTTPServer(('0.0.0.0', 8095), CloudManagerHandler).serve_forever()
