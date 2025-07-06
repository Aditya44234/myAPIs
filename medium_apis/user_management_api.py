from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import uuid
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# In-memory storage (replace with database in production)
users = {}
user_sessions = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
        except:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# 1. User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not all([email, password, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if email in [user['email'] for user in users.values()]:
        return jsonify({'error': 'Email already registered'}), 409
    
    user_id = str(uuid.uuid4())
    users[user_id] = {
        'id': user_id,
        'email': email,
        'password': generate_password_hash(password),
        'name': name,
        'created_at': datetime.datetime.now().isoformat(),
        'profile': {
            'bio': '',
            'avatar': '',
            'phone': '',
            'address': ''
        }
    }
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201

# 2. User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = None
    for u in users.values():
        if u['email'] == email:
            user = u
            break
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    })

# 3. Get User Profile
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'user': {
            'id': current_user['id'],
            'email': current_user['email'],
            'name': current_user['name'],
            'created_at': current_user['created_at'],
            'profile': current_user['profile']
        }
    })

# 4. Update User Profile
@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' in data:
        current_user['name'] = data['name']
    
    if 'profile' in data:
        current_user['profile'].update(data['profile'])
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': current_user['id'],
            'email': current_user['email'],
            'name': current_user['name'],
            'profile': current_user['profile']
        }
    })

# 5. Change Password
@app.route('/api/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not all([old_password, new_password]):
        return jsonify({'error': 'Missing old or new password'}), 400
    
    if not check_password_hash(current_user['password'], old_password):
        return jsonify({'error': 'Invalid old password'}), 401
    
    current_user['password'] = generate_password_hash(new_password)
    return jsonify({'message': 'Password changed successfully'})

# 6. Get All Users (Admin only)
@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user):
    # Simple admin check (in real app, use roles)
    if current_user['email'] != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user_list = []
    for user in users.values():
        user_list.append({
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at']
        })
    
    return jsonify({'users': user_list})

# 7. Delete User Account
@app.route('/api/account', methods=['DELETE'])
@token_required
def delete_account(current_user):
    user_id = current_user['id']
    del users[user_id]
    return jsonify({'message': 'Account deleted successfully'})

# 8. Search Users
@app.route('/api/users/search', methods=['GET'])
@token_required
def search_users(current_user):
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    results = []
    for user in users.values():
        if (query in user['name'].lower() or 
            query in user['email'].lower()):
            results.append({
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            })
    
    return jsonify({'users': results})

# 9. Upload Avatar (simulated)
@app.route('/api/avatar', methods=['POST'])
@token_required
def upload_avatar(current_user):
    # In real app, handle file upload
    data = request.json
    avatar_url = data.get('avatar_url', '')
    
    current_user['profile']['avatar'] = avatar_url
    return jsonify({
        'message': 'Avatar updated successfully',
        'avatar_url': avatar_url
    })

# 10. Get User Stats
@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    total_users = len(users)
    return jsonify({
        'total_users': total_users,
        'user_id': current_user['id'],
        'account_age_days': (datetime.datetime.now() - 
                           datetime.datetime.fromisoformat(current_user['created_at'])).days
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 