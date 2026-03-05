# Add this to your app.py to enable CORS and token-based auth
"""
Add these imports at the top of app.py:
from flask_cors import CORS
import jwt
from functools import wraps
import datetime
"""

# Configuration to add to app.py
CORS_CONFIG = '''
# ==================== CORS & JWT CONFIGURATION ====================
# Enable CORS for your frontend domains
CORS(app, supports_credentials=True, origins=[
    "http://localhost:8088",
    "http://127.0.0.1:8088",
    "https://humbu.store",
    "https://api.humbu.store",
    "http://localhost:3000",  # React dev server
    "http://localhost:5000"   # Alternative
])

# JWT Configuration
app.config['SECRET_KEY'] = 'imperial_omega_secret_key_change_in_production'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        # If no token, check for session (for web clients)
        if not token:
            if 'user_id' in session:
                return f(*args, **kwargs)
            else:
                # For API requests, return JSON instead of redirect
                if request.path.startswith('/api/'):
                    return jsonify({'message': 'Authentication required'}), 401
                # For web requests, redirect to login
                return redirect(url_for('login', next=request.url))
        
        try:
            # Verify token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# New login endpoint that returns JWT for API clients
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.password == hash_password(password):
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'village': user.village
            }
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# New register endpoint for API clients
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    # Create new user
    hashed = hash_password(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed,
        phone=data.get('phone', ''),
        village=data.get('village', 'Unknown'),
        role='user'
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate token
    token = jwt.encode({
        'user_id': new_user.id,
        'email': new_user.email,
        'role': new_user.role,
        'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role,
            'village': new_user.village
        }
    }), 201

# Modified village endpoint that works with both session and token
@app.route('/api/admin/villages', methods=['GET', 'POST'])
@token_required
def api_admin_villages(current_user=None):
    if request.method == 'POST':
        data = request.get_json()
        new_v = Village(
            name=data.get("name"),
            district=data.get("district"),
            region=data.get("region"),
            population=data.get("population", 0)
        )
        db.session.add(new_v)
        db.session.commit()
        return jsonify({"message": "Village added", "id": new_v.id})
    
    villages = Village.query.all()
    return jsonify([{
        "id": v.id,
        "name": v.name,
        "district": v.district,
        "region": v.region,
        "population": v.population
    } for v in villages])
'''
