"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Temporary in-memory storage (replace with database in production)
users_db = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'teacher1': {'password': 'teacher123', 'role': 'teacher'},
    'student1': {'password': 'student123', 'role': 'student'}
}

@bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = users_db.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'success': True,
        'token': f'token_{username}_{datetime.now().timestamp()}',
        'user': {
            'username': username,
            'role': user['role']
        }
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify JWT token"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'valid': False}), 401
    
    return jsonify({'valid': True}), 200
