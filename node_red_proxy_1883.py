#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
from datetime import datetime

class NodeREDProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Try to proxy to real Node-RED on 1880
        try:
            req = urllib.request.Request(f"http://localhost:1880{self.path}")
            with urllib.request.urlopen(req, timeout=2) as response:
                self.send_response(200)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except:
            # Show Imperial-branded Node-RED dashboard
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Imperial Node-RED Dashboard</title>
                <style>
                    body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; color: #fff; }
                    .header { background: #2d2d2d; padding: 20px; border-bottom: 3px solid #ff6b6b; }
                    .container { display: flex; height: calc(100vh - 80px); }
                    .sidebar { width: 250px; background: #2d2d2d; padding: 20px; }
                    .main { flex: 1; padding: 20px; overflow-y: auto; }
                    .card { background: #2d2d2d; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #ff6b6b; }
                    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }
                    .stat-card { background: #333; padding: 15px; border-radius: 8px; text-align: center; }
                    .stat-value { font-size: 24px; font-weight: bold; color: #4CAF50; }
                    .btn { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; border: none; cursor: pointer; }
                    .flow { background: #333; padding: 10px; margin: 5px 0; border-radius: 4px; display: flex; justify-content: space-between; }
                    .badge { background: #ff6b6b; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1 style="margin:0;">🔄 Imperial Node-RED (Port 1883)</h1>
                    <small>IoT & Workflow Automation Hub</small>
                </div>
                <div class="container">
                    <div class="sidebar">
                        <h3>Navigation</h3>
                        <div style="margin: 20px 0;">
                            <div class="flow">📊 Dashboard</div>
                            <div class="flow">🔧 Flows</div>
                            <div class="flow">📦 Nodes</div>
                            <div class="flow">📈 Monitoring</div>
                            <div class="flow">⚙️ Settings</div>
                        </div>
                        <hr>
                        <h3>Imperial Stats</h3>
                        <div class="stat-card" style="margin-bottom:10px;">
                            <div>Network Status</div>
                            <div class="stat-value">25/36</div>
                        </div>
                        <div class="stat-card">
                            <div>Portfolio</div>
                            <div class="stat-value">R10.94M</div>
                        </div>
                    </div>
                    <div class="main">
                        <div class="stats">
                            <div class="stat-card">
                                <div>Active Flows</div>
                                <div class="stat-value">7</div>
                            </div>
                            <div class="stat-card">
                                <div>Total Nodes</div>
                                <div class="stat-value">42</div>
                            </div>
                            <div class="stat-card">
                                <div>Messages/min</div>
                                <div class="stat-value">1,247</div>
                            </div>
                        </div>
                        
                        <div class="card">
                            <h2 style="margin-top:0;">Active Workflows</h2>
                            <div class="flow">
                                <span>🌾 Village Crop Monitor</span>
                                <span><span class="badge">ACTIVE</span></span>
                            </div>
                            <div class="flow">
                                <span>💰 Revenue Tracker</span>
                                <span><span class="badge">ACTIVE</span></span>
                            </div>
                            <div class="flow">
                                <span>🌍 SADC Sync</span>
                                <span><span class="badge">ACTIVE</span></span>
                            </div>
                            <div class="flow">
                                <span>🔐 Wealth Lock Monitor</span>
                                <span><span class="badge">ACTIVE</span></span>
                            </div>
                        </div>
                        
                        <div class="card">
                            <h2 style="margin-top:0;">IoT Devices</h2>
                            <div class="flow">
                                <span>🌡️ Temp Sensor - Malamulele</span>
                                <span>32°C</span>
                            </div>
                            <div class="flow">
                                <span>💧 Humidity - Thohoyandou</span>
                                <span>67%</span>
                            </div>
                            <div class="flow">
                                <span>⚡ Energy - Bindura</span>
                                <span>342 kWh</span>
                            </div>
                        </div>
                        
                        <a href="http://localhost:1880" class="btn">Go to Real Node-RED (Port 1880)</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        return

print("🔄 Node-RED Proxy starting on port 1883 (HTML Dashboard)")
HTTPServer(('0.0.0.0', 1883), NodeREDProxyHandler).serve_forever()
