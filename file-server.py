from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/')
def index():
    files = [f for f in os.listdir('.') if f.endswith('.hat')]
    return jsonify({
        "available_configs": files,
        "download_url": "/files/imperial-tunnel.hat",
        "status": "online"
    })

if __name__ == '__main__':
    print("📁 File server on port 8116")
    app.run(host='0.0.0.0', port=8116)
