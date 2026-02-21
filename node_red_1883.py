#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from datetime import datetime

class NodeREDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Simulate IoT and workflow data
        workflows = [
            {'id': 'flow_001', 'name': 'Village Monitor', 'status': 'active', 'nodes': 5},
            {'id': 'flow_002', 'name': 'Revenue Tracker', 'status': 'active', 'nodes': 3},
            {'id': 'flow_003', 'name': 'SADC Sync', 'status': 'idle', 'nodes': 7},
            {'id': 'flow_004', 'name': 'Wealth Lock', 'status': 'active', 'nodes': 4}
        ]
        
        iot_devices = [
            {'device': 'sensor_01', 'type': 'temperature', 'value': random.randint(20, 35), 'village': 'Malamulele'},
            {'device': 'sensor_02', 'type': 'humidity', 'value': random.randint(40, 80), 'village': 'Thohoyandou'},
            {'device': 'sensor_03', 'type': 'energy', 'value': random.randint(100, 500), 'village': 'Bindura'}
        ]
        
        response = {
            'service': 'Node-RED',
            'status': 'online',
            'version': '2.2.2',
            'workflows': workflows,
            'iot_devices': iot_devices,
            'stats': {
                'active_flows': 3,
                'total_nodes': 19,
                'messages_processed': random.randint(1000, 5000)
            },
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        return

print("🔄 Node-RED starting on port 1883...")
HTTPServer(('0.0.0.0', 1883), NodeREDHandler).serve_forever()
