"""
Admin Routes
"""
from flask import Blueprint, request, jsonify

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get admin dashboard data"""
    return jsonify({
        'total_students': 150,
        'total_teachers': 35,
        'total_assessments': 42,
        'active_sessions': 12,
        'last_sync': '2026-02-24T10:30:00Z'
    }), 200

@bp.route('/settings', methods=['GET'])
def get_settings():
    """Get system settings"""
    return jsonify({
        'school_name': 'Gaybeck Starkids',
        'version': '1.0.0',
        'ai_enabled': True,
        'features': {
            'assessments': True,
            'analytics': True,
            'sync': True
        }
    }), 200

@bp.route('/settings', methods=['PUT'])
def update_settings():
    """Update system settings"""
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'Settings updated successfully',
        'data': data
    }), 200

@bp.route('/backup', methods=['POST'])
def create_backup():
    """Create database backup"""
    return jsonify({
        'success': True,
        'message': 'Backup created successfully',
        'timestamp': '2026-02-24T10:35:00Z'
    }), 200

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get system logs"""
    return jsonify({
        'logs': [
            {'timestamp': '2026-02-24T10:30:00Z', 'level': 'INFO', 'message': 'User admin logged in'},
            {'timestamp': '2026-02-24T10:25:00Z', 'level': 'INFO', 'message': 'Assessment created'},
        ]
    }), 200
