"""
Teacher Routes
"""
from flask import Blueprint, request, jsonify

bp = Blueprint('teachers', __name__, url_prefix='/api/teachers')

# Temporary in-memory storage
teachers_db = {
    '1': {'id': '1', 'name': 'Mr. Johnson', 'subject': 'Mathematics', 'class': 'SS1'},
    '2': {'id': '2', 'name': 'Mrs. Williams', 'subject': 'English', 'class': 'SS2'}
}

@bp.route('/', methods=['GET'])
def get_teachers():
    """Get all teachers"""
    return jsonify(list(teachers_db.values())), 200

@bp.route('/<teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """Get specific teacher"""
    teacher = teachers_db.get(teacher_id)
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404
    return jsonify(teacher), 200

@bp.route('/', methods=['POST'])
def create_teacher():
    """Create new teacher"""
    data = request.get_json()
    new_id = str(len(teachers_db) + 1)
    teacher = {
        'id': new_id,
        'name': data.get('name'),
        'subject': data.get('subject'),
        'class': data.get('class')
    }
    teachers_db[new_id] = teacher
    return jsonify(teacher), 201

@bp.route('/<teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """Update teacher"""
    if teacher_id not in teachers_db:
        return jsonify({'error': 'Teacher not found'}), 404
    
    data = request.get_json()
    teachers_db[teacher_id].update(data)
    return jsonify(teachers_db[teacher_id]), 200

@bp.route('/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """Delete teacher"""
    if teacher_id not in teachers_db:
        return jsonify({'error': 'Teacher not found'}), 404
    
    del teachers_db[teacher_id]
    return jsonify({'success': True}), 200
