import http.server
import socketserver

PORT = 8093
TARGET = 500000000  # R500M
MILESTONE_1 = 50000000 # R50M
CURRENT = 7500000    # Verified Split

class VelocityHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        progress = (CURRENT / MILESTONE_1) * 100
        html = f"""
        <html>
        <head><title>🚀 Imperial Velocity</title>
        <style>
            body {{ background: #0a0f1e; color: #ffd700; font-family: sans-serif; text-align: center; }}
            .bar {{ background: #1a2635; width: 80%; margin: 20px auto; border-radius: 20px; height: 40px; border: 2px solid #ffd700; }}
            .fill {{ background: linear-gradient(90deg, #ffd700, #90EE90); width: {progress}%; height: 100%; border-radius: 18px; }}
        </style>
        </head>
        <body>
            <h1>🏆 PROGRESS TO R50M MILESTONE</h1>
            <div class="bar"><div class="fill"></div></div>
            <h2>{progress}% COMPLETE</h2>
            <p>Current Split: R7,500,000</p>
            <p>Remaining to 10%: R42,500,000</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

with socketserver.TCPServer(("", PORT), VelocityHandler) as httpd:
    print(f"🚀 Velocity Dashboard active on Port {PORT}")
    httpd.serve_forever()
