#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from datetime import datetime

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        conn = sqlite3.connect('instance/imperial.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM payment")
        payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM village")
        villages = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(amount) FROM payment WHERE status='completed'")
        revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        response = {
            'service': 'Apex_Metrics',
            'status': 'online',
            'users': users,
            'payments': payments,
            'villages': villages,
            'revenue': revenue,
            'portfolio': 10938044.07,
            'progress_pct': 313.6,
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

def run_server():
    server = HTTPServer(('0.0.0.0', 8086), MetricsHandler)
    print("📊 Apex Metrics running on port 8086")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
