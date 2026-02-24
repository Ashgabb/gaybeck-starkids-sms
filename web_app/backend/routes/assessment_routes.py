"""
AI Assessment Routes
"""
from flask import Blueprint, request, jsonify

bp = Blueprint('assessments', __name__, url_prefix='/api/assessments')

# Temporary in-memory storage
assessments_db = {
    '1': {
        'id': '1',
        'title': 'Mathematics Quiz',
        'subject': 'Math',
        'class': 'SS1',
        'difficulty': 'Medium',
        'question_count': 10,
        'teacher': 'Mr. Johnson'
    }
}

@bp.route('/', methods=['GET'])
def get_assessments():
    """Get all assessments"""
    return jsonify(list(assessments_db.values())), 200

@bp.route('/<assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """Get specific assessment"""
    assessment = assessments_db.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404
    return jsonify(assessment), 200

@bp.route('/', methods=['POST'])
def create_assessment():
    """Create new AI assessment"""
    data = request.get_json()
    new_id = str(len(assessments_db) + 1)
    assessment = {
        'id': new_id,
        'title': data.get('title'),
        'subject': data.get('subject'),
        'class': data.get('class'),
        'difficulty': data.get('difficulty', 'Medium'),
        'question_count': data.get('question_count', 10),
        'teacher': data.get('teacher')
    }
    assessments_db[new_id] = assessment
    return jsonify(assessment), 201

@bp.route('/<assessment_id>', methods=['PUT'])
def update_assessment(assessment_id):
    """Update assessment"""
    if assessment_id not in assessments_db:
        return jsonify({'error': 'Assessment not found'}), 404
    
    data = request.get_json()
    assessments_db[assessment_id].update(data)
    return jsonify(assessments_db[assessment_id]), 200

@bp.route('/<assessment_id>', methods=['DELETE'])
def delete_assessment(assessment_id):
    """Delete assessment"""
    if assessment_id not in assessments_db:
        return jsonify({'error': 'Assessment not found'}), 404
    
    del assessments_db[assessment_id]
    return jsonify({'success': True}), 200
