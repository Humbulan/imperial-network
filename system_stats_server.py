#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
from datetime import datetime

class SystemStatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            def call_rish(cmd):
                # Using -c flag for more reliable one-shot command execution
                result = subprocess.run(['./rish', '-c', cmd], capture_output=True, text=True, encoding='utf-8')
                return result.stdout.strip()

            battery_raw = call_rish("dumpsys battery")
            battery = {}
            for line in battery_raw.split('\n'):
                if 'level:' in line:
                    battery['level'] = int(line.split(':')[1].strip())
                elif 'status:' in line:
                    battery['status'] = line.split(':')[1].strip()
                elif 'temperature:' in line:
                    battery['temp_c'] = float(line.split(':')[1].strip()) / 10
            
            # Explicitly targeting Samsung-specific properties if standard ones fail
            model = call_rish("getprop ro.product.model")
            if not model:
                model = call_rish("getprop ro.product.odm.model")

            response = {
                'service': 'System_Stats',
                'status': 'online',
                'battery': battery,
                'device': {
                    'model': model if model else "SM-A736B",
                    'android_ver': call_rish("getprop ro.build.version.release"),
                    'sdk_ver': call_rish("getprop ro.build.version.sdk")
                },
                'timestamp': str(datetime.now())
            }
        except Exception as e:
            response = {'service': 'System_Stats', 'status': 'error', 'error': str(e)}
        
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8093), SystemStatsHandler)
    server.serve_forever()
