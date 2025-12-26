# Gaybeck Starkids SMS - Web Application

A modern Django-based web application for school management. This is a complete conversion of the desktop Tkinter application to a responsive web platform with all original features and enhanced capabilities.

## 🎯 Features

### Core Modules
- **👥 User Management** - Role-based access control (Admin, Teacher, Accountant)
- **🎓 Student Management** - Complete student profiles with document uploads
- **👨‍🏫 Teacher Management** - Teacher profiles and class assignments
- **📅 Attendance Tracking** - Daily attendance with multiple status options
- **💰 Fee Management** - Track fees, payments, and payment history
- **📊 Grading System** - Record and view student grades
- **📈 Analytics** - AI-powered insights and comprehensive reports
- **🎯 Dashboard** - Real-time statistics and activity monitoring

### Technical Features
- Responsive Bootstrap 5 UI
- Role-based access control
- Activity logging and auditing
- Pagination and filtering
- Image and document uploads
- Multiple payment method tracking
- Comprehensive admin interface

## 🚀 Quick Start

### Windows Users
```bash
cd web_app
setup.bat
python manage.py runserver
```

### Linux/Mac Users
```bash
cd web_app
chmod +x setup.sh
./setup.sh
python manage.py runserver
```

Then open `http://localhost:8000` in your browser.

## 📋 System Requirements

- Python 3.8 or higher
- SQLite3 (included with Python)
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 📦 Installation

### Step 1: Clone/Navigate to Project
```bash
cd web_app
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
```

### Step 5: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000`

## 🏗️ Architecture

```
web_app/
├── accounts/          # Authentication & User Management
│   ├── models.py      # User model with roles
│   ├── views.py       # Login, logout, profile views
│   ├── forms.py       # User forms
│   └── urls.py        # Account URLs
│
├── students/          # Student Management
│   ├── models.py      # Student and StudentDocument
│   ├── views.py       # CRUD operations
│   ├── forms.py       # Student forms
│   └── urls.py
│
├── teachers/          # Teacher Management
│   ├── models.py      # Teacher and ClassAssignment
│   ├── views.py
│   ├── admin.py
│   └── urls.py
│
├── attendance/        # Attendance Tracking
│   ├── models.py      # AttendanceRecord
│   ├── views.py       # Attendance views
│   ├── admin.py
│   └── urls.py
│
├── fees/             # Fee Management
│   ├── models.py     # FeeType, StudentFee, FeePayment
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── grading/          # Grading System
│   ├── models.py     # Grade model
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── analytics/        # Analytics & Reports
│   ├── models.py     # StudentAnalytics, ClassAnalytics
│   ├── views.py      # Dashboard views
│   └── urls.py
│
├── dashboard/        # Main Dashboard
│   ├── views.py      # Dashboard view
│   └── urls.py
│
├── config/           # Django Configuration
│   ├── settings.py   # Main settings
│   ├── urls.py       # URL routing
│   ├── wsgi.py       # WSGI config
│   └── asgi.py       # ASGI config
│
├── templates/        # HTML Templates
│   ├── base.html     # Base template
│   ├── accounts/     # Auth templates
│   ├── students/     # Student templates
│   ├── attendance/   # Attendance templates
│   ├── fees/        # Fee templates
│   ├── grading/     # Grade templates
│   ├── analytics/   # Analytics templates
│   └── dashboard/   # Dashboard templates
│
├── static/          # CSS, JavaScript, Images
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── manage.py        # Django CLI
├── requirements.txt # Python dependencies
├── .env.example     # Environment template
├── Dockerfile       # Docker configuration
├── docker-compose.yml # Docker Compose config
└── QUICKSTART.md    # Quick start guide
```

## 🔐 Default Roles

### Administrator
- Full system access
- User management
- All module access
- Admin interface access

### Teacher
- View assigned classes
- Record attendance
- Enter grades
- View student performance

### Accountant
- Manage fees
- Record payments
- View fee reports
- Track financial status

## 🗄️ Database Schema

### Core Tables
- **User** - System users with role-based access
- **Student** - Student information and enrollment
- **Teacher** - Teacher profiles and assignments
- **AttendanceRecord** - Daily attendance tracking
- **StudentFee** - Fee assignments and tracking
- **FeePayment** - Payment records
- **Grade** - Student grades per subject
- **ClassAssignment** - Teacher-class-subject assignments
- **ActivityLog** - User activity auditing
- **AnalyticsReport** - Generated reports

## 📱 Screenshots Preview

### Dashboard
Main overview with statistics and recent activities

### Student Management
List, add, edit, and view student information

### Attendance
Record and view attendance with multiple statuses

### Fee Management
Track student fees and payment status

### Analytics
View insights and performance metrics

## ⚙️ Configuration

### Environment Variables
```
SECRET_KEY          # Django secret key
DEBUG               # Debug mode (False in production)
ALLOWED_HOSTS       # Allowed domains
DATABASE_URL        # Database connection string
EMAIL_BACKEND       # Email configuration
```

### Settings File
Edit `config/settings.py` for advanced configuration:
- Database settings
- Installed apps
- Middleware
- Template configuration
- Static files
- Media files

## 🚀 Deployment

### Gunicorn (Production WSGI Server)
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Docker
```bash
docker build -t sms-webapp .
docker run -p 8000:8000 sms-webapp
```

### Docker Compose
```bash
docker-compose up
```

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Update `SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use PostgreSQL or MySQL
- [ ] Enable HTTPS
- [ ] Set up environment variables
- [ ] Configure email backend
- [ ] Set up backup strategy
- [ ] Enable logging
- [ ] Configure CORS for external access

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

Create test data:
```bash
python manage.py shell < scripts/create_sample_data.py
```

## 📚 API Documentation

### Student Endpoints
- `GET /students/` - List all students
- `POST /students/create/` - Create student
- `GET /students/<id>/` - Get student detail
- `POST /students/<id>/edit/` - Edit student
- `GET /students/<id>/delete/` - Delete student

### Attendance Endpoints
- `GET /attendance/` - List attendance
- `GET /attendance/date/<date>/` - By date
- `GET /attendance/class/<class>/` - By class
- `GET /attendance/student/<id>/` - By student

### Fees Endpoints
- `GET /fees/` - List fees
- `GET /fees/student/<id>/` - Student fees
- `POST /fees/<id>/pay/` - Record payment

### Grading Endpoints
- `GET /grading/` - List grades
- `GET /grading/student/<id>/` - Student grades
- `POST /grading/create/` - Add grade

## 🔧 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Lock
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Permission Issues
```bash
chmod +x manage.py
chmod +x setup.sh
```

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🤝 Contributing

To contribute improvements:
1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

© 2024-2025 Gaybeck Starkids School. All rights reserved.

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Quick Start Guide](QUICKSTART.md)
3. Contact system administrator

## 🎓 Version

- **Current**: Web v1.0
- **Python**: 3.8+
- **Django**: 4.2+
- **Bootstrap**: 5.3+

---

**Last Updated**: December 2024
**Status**: Production Ready
