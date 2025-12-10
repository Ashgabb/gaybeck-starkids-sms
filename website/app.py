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
    
    print("""
    ╔════════════════════════════════════════════╗
    ║  Gaybeck Starkids SMS - Website API Server ║
    ║  Status: ✅ RUNNING                        ║
    ║  URL: http://localhost:5000                ║
    ║  API Docs: http://localhost:5000/api/docs  ║
    ╚════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
