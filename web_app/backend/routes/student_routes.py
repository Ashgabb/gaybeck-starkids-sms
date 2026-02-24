"""
Student Routes
"""
from flask import Blueprint, request, jsonify

bp = Blueprint('students', __name__, url_prefix='/api/students')

# Temporary in-memory storage
students_db = {
    '1': {'id': '1', 'name': 'John Doe', 'class': 'SS1', 'email': 'john@school.com'},
    '2': {'id': '2', 'name': 'Jane Smith', 'class': 'SS1', 'email': 'jane@school.com'}
}

@bp.route('/', methods=['GET'])
def get_students():
    """Get all students"""
    return jsonify(list(students_db.values())), 200

@bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get specific student"""
    student = students_db.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student), 200

@bp.route('/', methods=['POST'])
def create_student():
    """Create new student"""
    data = request.get_json()
    new_id = str(len(students_db) + 1)
    student = {
        'id': new_id,
        'name': data.get('name'),
        'class': data.get('class'),
        'email': data.get('email')
    }
    students_db[new_id] = student
    return jsonify(student), 201

@bp.route('/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student"""
    if student_id not in students_db:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    students_db[student_id].update(data)
    return jsonify(students_db[student_id]), 200

@bp.route('/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student"""
    if student_id not in students_db:
        return jsonify({'error': 'Student not found'}), 404
    
    del students_db[student_id]
    return jsonify({'success': True}), 200
