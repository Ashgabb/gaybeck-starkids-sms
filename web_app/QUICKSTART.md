# Gaybeck Starkids SMS - Web App Quick Start Guide

## Overview
This is a Django-based web application conversion of the Tkinter desktop SMS system. It maintains all core features with a modern, responsive web interface.

## Features
- **User Management**: Admin, Teacher, and Accountant roles
- **Student Management**: Full CRUD operations with document uploads
- **Attendance Tracking**: Daily attendance records with status tracking
- **Fee Management**: Track fees, payments, and payment history
- **Grading System**: Record and track student grades
- **Analytics**: AI-powered insights and reports
- **Dashboard**: Real-time statistics and recent activities

## Requirements
- Python 3.8+
- SQLite3 (included with Python)
- pip (Python package manager)

## Quick Setup (Windows)

### 1. Run Setup Script
```bash
setup.bat
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the database
- Create a superuser account

### 2. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser

## Quick Setup (Linux/Mac)

### 1. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Run Development Server
```bash
python manage.py runserver
```

## Manual Setup (If Scripts Don't Work)

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env File
```
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Run Server
```bash
python manage.py runserver
```

## Default Login
- Navigate to `http://localhost:8000/accounts/login/`
- Use the superuser credentials you created during setup

## Admin Interface
- Access Django admin at `http://localhost:8000/admin/`
- Use superuser credentials

## Directory Structure
```
web_app/
├── accounts/           # User authentication and management
├── students/           # Student management
├── teachers/           # Teacher management
├── attendance/         # Attendance tracking
├── fees/              # Fee management
├── grading/           # Grade management
├── analytics/         # Analytics and reports
├── dashboard/         # Main dashboard
├── config/            # Django settings
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Deployment

### Using Gunicorn (Production)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

1. Build image:
```bash
docker build -t sms-webapp .
```

2. Run container:
```bash
docker run -p 8000:8000 sms-webapp
```

## Environment Variables (Production)

Set these before deployment:
```
SECRET_KEY=your-very-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/smsdb
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Permission Denied (Linux/Mac)
```bash
chmod +x manage.py
chmod +x setup.sh
```

## Creating Sample Data

Use Django shell:
```bash
python manage.py shell
```

```python
from students.models import Student
from datetime import date

Student.objects.create(
    name='John Doe',
    registration_number='STU001',
    date_of_birth=date(2010, 1, 1),
    gender='M',
    email='john@example.com',
    phone='254700000000',
    address='123 Main St',
    class_name='Form 1A',
    guardian_name='Jane Doe',
    guardian_phone='254700000001'
)
```

## Support
For issues or questions, check the Django documentation at https://docs.djangoproject.com/
