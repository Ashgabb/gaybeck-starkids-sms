"""
Gaybeck Starkids SMS - Flask Backend API
Main application entry point
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Import blueprints
from routes import auth_routes, student_routes, teacher_routes, assessment_routes, admin_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(student_routes.bp)
app.register_blueprint(teacher_routes.bp)
app.register_blueprint(assessment_routes.bp)
app.register_blueprint(admin_routes.bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Gaybeck Starkids SMS API',
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
