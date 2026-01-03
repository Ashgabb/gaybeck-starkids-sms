"""
Gaybeck Starkids SMS - Website Backend API
Provides REST API endpoints for website functionality
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='website', static_url_path='')
CORS(app)

# Configuration
DATABASE = 'database/school_management.db'
WEBSITE_FOLDER = 'website'

# ===== DATABASE HELPERS =====
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# ===== STATIC FILES =====
@app.route('/')
def index():
    return send_from_directory(WEBSITE_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(WEBSITE_FOLDER, filename)

# ===== API ENDPOINTS =====

# Health Check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat()
    })

# Get System Statistics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db()
        
        stats = {
            'total_students': conn.execute('SELECT COUNT(*) FROM students').fetchone()[0],
            'total_teachers': conn.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
            'total_classes': conn.execute('SELECT COUNT(*) FROM classes').fetchone()[0],
            'total_fees_collected': conn.execute('SELECT COALESCE(SUM(amount_paid), 0) FROM financial_records WHERE status="Paid"').fetchone()[0],
            'pending_fees': conn.execute('SELECT COALESCE(SUM(amount_due), 0) FROM fees WHERE status="Pending"').fetchone()[0],
        }
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Contact Form Submission
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        
        # Validate
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Save to database
        conn = get_db()
        conn.execute('''
            INSERT INTO contacts (name, email, phone, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('email'),
            data.get('phone', ''),
            data.get('subject', 'Website Contact'),
            data.get('message'),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Message received! We will contact you soon.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download App
@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.json
        
        # Log download request
        conn = get_db()
        conn.execute('''
            INSERT INTO downloads (email, os, version, downloaded_at)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('email', 'unknown'),
            data.get('os', 'unknown'),
            '2.0.3',
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        # Return download link
        return jsonify({
            'status': 'success',
            'download_url': 'GAYBECK_STARKIDS_SMS_20251204_201507.zip',
            'message': 'Download starting...'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Newsletter Signup
@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        conn = get_db()
        
        # Check if already subscribed
        existing = conn.execute(
            'SELECT * FROM newsletter_subscribers WHERE email = ?',
            (email,)
        ).fetchone()
        
        if existing:
            return jsonify({
                'status': 'info',
                'message': 'Already subscribed!'
            })
        
        # Add subscriber
        conn.execute('''
            INSERT INTO newsletter_subscribers (email, subscribed_at)
            VALUES (?, ?)
        ''', (email, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully subscribed to newsletter!'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Pricing Info
@app.route('/api/pricing', methods=['GET'])
def pricing():
    pricing_tiers = [
        {
            'name': 'Free Trial',
            'price': 'GHS 0',
            'duration': '30 days',
            'features': [
                'All core features',
                'Up to 100 students',
                'Up to 10 teachers',
                'Email support',
                'No credit card required'
            ]
        },
        {
            'name': 'Professional',
            'price': 'GHS 500',
            'duration': 'One-time payment',
            'features': [
                'All features included',
                'Unlimited students',
                'Unlimited teachers',
                'Priority support',
                'Advanced analytics',
                'Automatic backups',
                'Custom branding'
            ],
            'featured': True
        },
        {
            'name': 'Enterprise',
            'price': 'Custom',
            'duration': 'Contact sales',
            'features': [
                'Custom deployment',
                'API access',
                'Dedicated support',
                'Custom features',
                'Multi-school support',
                'On-premise hosting',
                'Training included'
            ]
        }
    ]
    return jsonify(pricing_tiers)

# Get Features
@app.route('/api/features', methods=['GET'])
def features():
    features_list = [
        {
            'icon': '👨‍🎓',
            'title': 'Student Management',
            'description': 'Complete student profiles with personal, academic, and medical information'
        },
        {
            'icon': '👨‍🏫',
            'title': 'Teacher Management',
            'description': 'Staff directory, qualifications, salary tracking, and document management'
        },
        {
            'icon': '📋',
            'title': 'Attendance System',
            'description': 'Real-time attendance tracking with comprehensive reports'
        },
        {
            'icon': '💰',
            'title': 'Financial Management',
            'description': 'Fee tracking, invoicing, payment records, and financial reports'
        },
        {
            'icon': '📊',
            'title': 'Grade Management',
            'description': 'Record and track student grades with performance analysis'
        },
        {
            'icon': '🔐',
            'title': 'Role-Based Access',
            'description': 'Secure access control for Admin, Teacher, and Accountant roles'
        }
    ]
    return jsonify(features_list)

# Get Modules
@app.route('/api/modules', methods=['GET'])
def modules():
    modules_list = [
        {
            'name': 'Academic Module',
            'icon': '📚',
            'features': ['Class management', 'Subject tracking', 'Assignment management', 'Grade recording', 'Report cards']
        },
        {
            'name': 'Student Module',
            'icon': '👨‍🎓',
            'features': ['Student profiles', 'Enrollment', 'Progress tracking', 'Medical records', 'Parental info']
        },
        {
            'name': 'Attendance Module',
            'icon': '📋',
            'features': ['Mark attendance', 'Track records', 'Generate reports', 'Absence alerts', 'Statistics']
        },
        {
            'name': 'Financial Module',
            'icon': '💰',
            'features': ['Fee management', 'Invoicing', 'Payment tracking', 'Financial reports', 'Accounting']
        },
        {
            'name': 'Grade Module',
            'icon': '📊',
            'features': ['Grade recording', 'Performance analysis', 'Report generation', 'Grade distribution', 'Trends']
        },
        {
            'name': 'Reports Module',
            'icon': '📄',
            'features': ['Custom reports', 'Data export', 'PDF generation', 'Scheduled reports', 'Analytics']
        }
    ]
    return jsonify(modules_list)

# Get Requirements
@app.route('/api/requirements', methods=['GET'])
def requirements():
    reqs = {
        'os': 'Windows 7, 8, 10, 11 or newer',
        'ram': '4 GB minimum (8 GB recommended)',
        'storage': '500 MB free space',
        'processor': 'Dual-core processor or better',
        'network': 'Internet connection (optional for sync)',
        'python': 'Python 3.13.x',
        'browser': 'Chrome, Firefox, Safari, or Edge'
    }
    return jsonify(reqs)

# Get Testimonials
@app.route('/api/testimonials', methods=['GET'])
def testimonials():
    testimonials_list = [
        {
            'name': 'Principal John Mensah',
            'school': 'Accra International School',
            'rating': 5,
            'quote': 'Gaybeck Starkids SMS transformed how we manage our school. It\'s comprehensive, user-friendly, and affordable!'
        },
        {
            'name': 'Mrs. Ama Osei',
            'school': 'Kumasi Academy',
            'rating': 5,
            'quote': 'The best investment we made for our school. All our data is organized and accessible. Highly recommended!'
        },
        {
            'name': 'Mr. Kwesi Darkoh',
            'school': 'Tema Central School',
            'rating': 5,
            'quote': 'Excellent support team and fantastic system. Our office staff productivity has increased significantly.'
        }
    ]
    return jsonify(testimonials_list)

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ===== RUN =====
if __name__ == '__main__':
    # Create required tables if they don't exist
    conn = get_db()
    
    # Contact table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Downloads table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            os TEXT,
            version TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Newsletter subscribers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# ===== DEMO DATA ENDPOINTS =====

# Demo Students
@app.route('/api/demo/students', methods=['GET'])
def demo_students():
    """Return sample student data for website demo"""
    students = [
        {'id': 'STU001', 'name': 'Ama Mensah', 'class': 'Form 2A', 'gender': 'Female', 'dob': '2008-03-15', 'status': 'Active'},
        {'id': 'STU002', 'name': 'Kwame Osei', 'class': 'Form 2A', 'gender': 'Male', 'dob': '2008-05-22', 'status': 'Active'},
        {'id': 'STU003', 'name': 'Abena Kusi', 'class': 'Form 1B', 'gender': 'Female', 'dob': '2009-07-10', 'status': 'Active'},
        {'id': 'STU004', 'name': 'Kofi Agyeman', 'class': 'Form 1A', 'gender': 'Male', 'dob': '2009-02-14', 'status': 'Active'},
        {'id': 'STU005', 'name': 'Efua Boateng', 'class': 'Form 2B', 'gender': 'Female', 'dob': '2008-11-20', 'status': 'Active'},
        {'id': 'STU006', 'name': 'Benjamin Addo', 'class': 'Form 1B', 'gender': 'Male', 'dob': '2009-04-08', 'status': 'Active'},
        {'id': 'STU007', 'name': 'Yaa Asante', 'class': 'Form 2B', 'gender': 'Female', 'dob': '2008-08-30', 'status': 'Active'},
        {'id': 'STU008', 'name': 'Akosua Debrah', 'class': 'Form 1A', 'gender': 'Female', 'dob': '2009-01-25', 'status': 'Active'},
    ]
    return jsonify(students)

# Demo Attendance
@app.route('/api/demo/attendance/<class_name>', methods=['GET'])
def demo_attendance(class_name):
    """Return sample attendance data"""
    attendance_data = {
        'Form 1A': [
            {'student': 'Kofi Agyeman', 'status': 'Present', 'time': '08:00 AM', 'notes': '-'},
            {'student': 'Akosua Debrah', 'status': 'Present', 'time': '08:02 AM', 'notes': '-'},
            {'student': 'John Mensah', 'status': 'Late', 'time': '08:35 AM', 'notes': 'Traffic'},
            {'student': 'Mary Owusu', 'status': 'Absent', 'time': '-', 'notes': 'Sick leave'},
            {'student': 'Samuel Boateng', 'status': 'Present', 'time': '08:01 AM', 'notes': '-'},
        ],
        'Form 1B': [
            {'student': 'Abena Kusi', 'status': 'Present', 'time': '08:00 AM', 'notes': '-'},
            {'student': 'Benjamin Addo', 'status': 'Present', 'time': '08:02 AM', 'notes': '-'},
            {'student': 'Victoria Asante', 'status': 'Excused', 'time': '-', 'notes': 'Medical'},
        ],
        'Form 2A': [
            {'student': 'Ama Mensah', 'status': 'Present', 'time': '08:00 AM', 'notes': '-'},
            {'student': 'Kwame Osei', 'status': 'Present', 'time': '08:01 AM', 'notes': '-'},
        ]
    }
    return jsonify(attendance_data.get(class_name, []))

# Demo Grades
@app.route('/api/demo/grades/<student_id>', methods=['GET'])
def demo_grades(student_id):
    """Return sample grade data"""
    grades = [
        {'subject': 'Mathematics', 'test1': 75, 'test2': 82, 'exam': 88, 'final': 82, 'grade': 'A'},
        {'subject': 'English', 'test1': 88, 'test2': 90, 'exam': 85, 'final': 88, 'grade': 'A'},
        {'subject': 'Science', 'test1': 70, 'test2': 76, 'exam': 80, 'final': 76, 'grade': 'B'},
        {'subject': 'Social Studies', 'test1': 92, 'test2': 88, 'exam': 91, 'final': 90, 'grade': 'A'},
    ]
    return jsonify(grades)

# Demo Analytics
@app.route('/api/demo/analytics', methods=['GET'])
def demo_analytics():
    """Return sample analytics data"""
    analytics = {
        'at_risk_students': 8,
        'top_performers': 23,
        'attendance_rate': 92.5,
        'revenue_forecast': 156000,
        'fee_collection_rate': 78.3,
        'grade_distribution': {
            'A': 45,
            'B': 68,
            'C': 92,
            'D': 35,
            'F': 10
        },
        'class_performance': {
            'Form 1A': 76.5,
            'Form 1B': 81.2,
            'Form 2A': 84.3,
            'Form 2B': 79.8
        }
    }
    return jsonify(analytics)

# Demo Financial
@app.route('/api/demo/financial', methods=['GET'])
def demo_financial():
    """Return sample financial data"""
    financial = {
        'total_fees_due': 125450,
        'amount_collected': 98200,
        'outstanding_balance': 27250,
        'collection_rate': 78.3,
        'recent_payments': [
            {'date': '2025-01-03', 'student': 'Kwame Mensah', 'amount': 500, 'method': 'Bank Transfer', 'status': 'Cleared'},
            {'date': '2025-01-02', 'student': 'Ama Asante', 'amount': 750, 'method': 'Mobile Money', 'status': 'Cleared'},
            {'date': '2025-01-01', 'student': 'Abena Owusu', 'amount': 500, 'method': 'Cash', 'status': 'Cleared'},
        ]
    }
    return jsonify(financial)

# API Documentation
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Return API documentation"""
    docs = {
        'title': 'Gaybeck Starkids SMS - Website API',
        'version': '2.0.3',
        'base_url': 'http://localhost:5000/api',
        'endpoints': [
            {
                'path': '/health',
                'method': 'GET',
                'description': 'Check API server health',
                'response': {'status': 'ok', 'message': 'Server is running'}
            },
            {
                'path': '/stats',
                'method': 'GET',
                'description': 'Get system statistics',
                'response': {'total_students': 250, 'total_teachers': 45, 'total_classes': 12}
            },
            {
                'path': '/demo/students',
                'method': 'GET',
                'description': 'Get sample student data',
                'response': 'Array of student objects'
            },
            {
                'path': '/demo/attendance/<class_name>',
                'method': 'GET',
                'description': 'Get sample attendance data for a class',
                'response': 'Array of attendance records'
            },
            {
                'path': '/demo/grades/<student_id>',
                'method': 'GET',
                'description': 'Get sample grade data for a student',
                'response': 'Array of grade records'
            },
            {
                'path': '/demo/analytics',
                'method': 'GET',
                'description': 'Get sample analytics data',
                'response': 'Analytics object with insights'
            },
            {
                'path': '/demo/financial',
                'method': 'GET',
                'description': 'Get sample financial data',
                'response': 'Financial summary object'
            }
        ]
    }
    return jsonify(docs)

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║  Gaybeck Starkids SMS - Website API Server ║
    ║  Status: ✅ RUNNING                        ║
    ║  URL: http://localhost:5000                ║
    ║  API Docs: http://localhost:5000/api/docs  ║
    ║  Demo: http://localhost:5000                ║
