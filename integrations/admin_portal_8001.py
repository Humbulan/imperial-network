import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class AdminHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>🏛️ Imperial Admin Portal</title>
            <style>
                body { background: #1a2635; color: white; font-family: monospace; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: #2d3a5e; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffd700; }
                .success { color: #90EE90; }
                .warning { color: #ffd700; }
                .terminal { background: #0a0f1e; padding: 15px; border-radius: 5px; font-family: monospace; }
                .btn { background: #ffd700; color: #1a2635; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
            </style>
            </head>
            <body>
            <div class="container">
                <h1>🏛️ IMPERIAL ADMIN PORTAL</h1>
                <div class="card">
                    <h2 class="warning">🔒 SOVEREIGN CONTROL PANEL</h2>
                    <p>Port 8001 - Control Plane Active</p>
                    <p>Status: <span class="success">🟢 ONLINE</span></p>
                </div>
                <div class="card">
                    <h3>📜 DIGITAL CONTRACT LEDGER</h3>
                    <div class="terminal" id="ledger">Loading ledger...</div>
                </div>
                <div class="card">
                    <h3>✍️ SIGN NEW CONTRACT</h3>
                    <p>Contract Ref: <span id="contractRef">SPLIT-2026-001</span></p>
                    <p>Growth Split: R7,500,000</p>
                    <button class="btn" onclick="signContract()">✍️ SIGN & EXECUTE</button>
                </div>
            </div>
            <script>
                function signContract() {
                    fetch('/api/contract/sign', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            contract_ref: 'SPLIT-2026-001',
                            timestamp: new Date().toISOString(),
                            split_verification: { growth: 7500000 }
                        })
                    })
                    .then(r => r.json())
                    .then(d => {
                        alert('✅ ' + d.message);
                        location.reload();
                    });
                }
                
                // Load ledger
                fetch('/api/ledger')
                    .then(r => r.json())
                    .then(d => {
                        document.getElementById('ledger').innerHTML = d.logs.join('<br>');
                    });
            </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/api/ledger':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            logs = []
            if os.path.exists('logs/contract_ledger.log'):
                with open('logs/contract_ledger.log', 'r') as f:
                    logs = f.readlines()[-10:]  # Last 10 entries
            self.wfile.write(json.dumps({"logs": [l.strip() for l in logs]}).encode())
    
    def do_POST(self):
        if self.path == '/api/contract/sign':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            # Log the signature to the Imperial Ledger
            timestamp = datetime.now().isoformat()
            contract_ref = post_data.get('contract_ref', 'UNKNOWN')
            growth = post_data.get('split_verification', {}).get('growth', 0)
            
            ledger_entry = f"{timestamp} - {contract_ref} - SIGNED - Growth Split: R{growth}"
            print(f"\n✍️ {ledger_entry}")
            
            # Ensure logs directory exists
            os.makedirs('logs', exist_ok=True)
            
            # Append to ledger
            with open('logs/contract_ledger.log', 'a') as f:
                f.write(ledger_entry + '\n')
            
            # Update wealth lock
            try:
                with open('wealth_lock.json', 'r+') as f:
                    wealth = json.load(f)
                    wealth['contracts_signed'] = wealth.get('contracts_signed', 0) + 1
                    wealth['last_split'] = growth
                    wealth['last_signature'] = timestamp
                    f.seek(0)
                    json.dump(wealth, f, indent=2)
                    f.truncate()
            except:
                pass

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "SUCCESS", 
                "message": "Contract Executed",
                "ledger_entry": ledger_entry
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AdminHandler)
    print(f"\n🏛️ ADMIN PORTAL UPGRADED ON PORT {port}")
    print(f"📜 Ledger: ~/imperial_network/logs/contract_ledger.log")
    print(f"🌐 Access at: http://localhost:{port}")
    print("=" * 50)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
