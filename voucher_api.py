#!/usr/bin/env python3
"""
🌐 Voucher API Server - Connects website to voucher system
Run on port 8098 or similar
"""
from flask import Flask, request, jsonify, render_template_string
from voucher_system import VoucherSystem
import json

app = Flask(__name__)
vs = VoucherSystem()

# Simple HTML form for testing
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Imperial AI - Voucher Activation</title>
    <style>
        body { font-family: Arial; padding: 40px; background: #f5f5f5; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; width: 100%; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎫 Activate AI Access</h2>
        <p>Enter your voucher code (format: XXXX-XXXX)</p>
        <input type="text" id="code" placeholder="e.g., ABCD-1234">
        <button onclick="activate()">Activate</button>
        <div id="result"></div>
    </div>
    <script>
        function activate() {
            let code = document.getElementById('code').value;
            fetch('/api/activate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(r => r.json())
            .then(d => {
                let div = document.getElementById('result');
                if(d.success) {
                    div.innerHTML = '<p class="success">✅ ' + d.message + '</p>';
                } else {
                    div.innerHTML = '<p class="error">❌ ' + d.message + '</p>';
                }
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_FORM

@app.route('/api/activate', methods=['POST'])
def activate():
    data = request.json
    code = data.get('code', '').strip().upper()
    
    # Remove any spaces and format
    code = code.replace(' ', '')
    if len(code) == 8:
        code = f"{code[:4]}-{code[4:]}"
    
    result = vs.use_voucher(code, ip_address=request.remote_addr)
    
    if result.get('success'):
        return jsonify({'success': True, 'message': f'Activated! You have {result["minutes"]} minutes of AI access.'})
    else:
        return jsonify({'success': False, 'message': result.get('reason', 'Invalid code')})

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.json
    code = data.get('code', '').strip().upper()
    code = code.replace(' ', '')
    if len(code) == 8:
        code = f"{code[:4]}-{code[4:]}"
    
    result = vs.validate_voucher(code)
    if result.get('valid'):
        return jsonify({'valid': True, 'value': result['value']})
    else:
        return jsonify({'valid': False, 'reason': result.get('reason', 'Invalid')})

@app.route('/api/stats')
def stats():
    return jsonify(vs.get_stats())

if __name__ == '__main__':
    print("🎫 Voucher API Server running on port 8098")
    print("   Use this for AI voucher activation")
    app.run(host='0.0.0.0', port=8098, debug=False)

@app.route('/api/create-voucher', methods=['POST'])
def create_voucher_from_payment():
    """Create a voucher after successful Yoco payment"""
    data = request.json
    payment_id = data.get('paymentId')
    
    # Create a new voucher
    code = vs.create_voucher(20, 30)
    # Add notes about payment
    conn = sqlite3.connect('vouchers.db')
    c = conn.cursor()
    c.execute("UPDATE vouchers SET notes=? WHERE code=?", (f'Yoco payment {payment_id}', code))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'code': code})
