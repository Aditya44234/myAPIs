from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/users')

# In-memory user store: {username: {password_hash, email}}
USERS = {}

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user. Expects JSON: username, password, email."""
    data = request.json
    if not data:
        return jsonify(error='No data provided'), 400
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        return jsonify(error='Missing fields'), 400
    if username in USERS:
        return jsonify(error='User exists'), 400
    USERS[username] = {
        'password_hash': generate_password_hash(password),
        'email': email
    }
    return jsonify(message='User registered!')

@user_bp.route('/login', methods=['POST'])
def login():
    """Login a user. Expects JSON: username, password."""
    data = request.json
    if not data:
        return jsonify(error='No data provided'), 400
    username = data.get('username')
    password = data.get('password')
    user = USERS.get(username)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify(error='Invalid credentials'), 401
    return jsonify(message='Login successful!')

@user_bp.route('/', methods=['GET'])
def list_users():
    """List all users (usernames and emails only)."""
    return jsonify(users=[{'username': u, 'email': info['email']} for u, info in USERS.items()])

@user_bp.route('/<username>', methods=['GET'])
def user_detail(username):
    """Get details for a user (username, email)."""
    user = USERS.get(username)
    if not user:
        return jsonify(error='User not found'), 404
    return jsonify(username=username, email=user['email'])

@user_bp.route('/<username>', methods=['DELETE'])
def delete_user(username):
    """Delete a user by username."""
    if username in USERS:
        del USERS[username]
        return jsonify(message='User deleted!')
    return jsonify(error='User not found'), 404 