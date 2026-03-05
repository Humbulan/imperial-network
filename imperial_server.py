from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

VOUCHER_FILE = 'vouchers.json'
if os.path.exists(VOUCHER_FILE):
    with open(VOUCHER_FILE) as f:
        vouchers = json.load(f)
else:
    vouchers = {"KCQK-L4G6": 20}
    with open(VOUCHER_FILE, 'w') as f:
        json.dump(vouchers, f)

@app.route('/api/validate-voucher', methods=['POST', 'OPTIONS'])
def validate_voucher():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    code = data.get('code', '').upper().strip()
    print(f"Validating voucher: {code}")  # This will show in logs
    if code in vouchers:
        return jsonify({"valid": True, "value": vouchers[code]})
    return jsonify({"valid": False})

@app.route('/api/ping')
def ping():
    return jsonify({"status": "online", "message": "Server is running"})

@app.route('/api/vouchers')
def list_vouchers():
    return jsonify(vouchers)

if __name__ == '__main__':
    print("Starting Imperial Server with API endpoints:")
    print("  - POST /api/validate-voucher")
    print("  - GET  /api/ping")
    print("  - GET  /api/vouchers")
    app.run(host='0.0.0.0', port=8098)
