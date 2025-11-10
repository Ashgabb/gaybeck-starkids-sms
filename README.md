# School Management System

**Version:** 2.0.0  
**Build Date:** November 10, 2025  
**Python Version:** 3.13+

## Overview

A comprehensive school management system with AI-powered analytics, built with Python and Tkinter. Features include student management, teacher management, attendance tracking, fee collection, grading system, and AI-driven insights for predictive analytics.

## Features

### Core Functionality
- 👥 **Student Management** - Complete student records with documents and photos
- 👨‍🏫 **Teacher Management** - Teacher profiles, assignments, and documents
- 📚 **Class Management** - Class organization and student assignment
- 📊 **Attendance Tracking** - Daily attendance with pattern analysis
- 💰 **Fee Management** - Fee collection, arrears tracking, and payment history
- 📝 **Grading System** - Assignment grading and performance tracking
- 📈 **Promotions** - Student promotion tracking across academic years

### Advanced Features
- 🤖 **AI Insights** - Machine learning-powered predictions
  - Attendance risk analysis
  - Fee payment risk detection
  - Student performance trends
  - Class-wide analytics
- 📋 **AI Report Generation** - Automated report creation with recommendations
- 💼 **Financial Management** - Income/expense tracking and budgeting
- 🔐 **User Management** - Role-based access control (Admin, Teacher, Accountant, Staff)
- 📱 **Responsive Design** - Adapts to different screen sizes
- 🖨️ **PDF Exports** - Generate printable reports
- 💾 **Backup & Restore** - Database backup and recovery system

## Installation

### Prerequisites
- Python 3.13 or higher
- Windows OS (tested on Windows 10/11)

### Required Packages
```bash
pip install -r requirements.txt
```

### Optional Packages (for AI features)
```bash
pip install scikit-learn pandas numpy
```

### Installation Steps

1. **Clone or extract** the application to your desired location

2. **Install dependencies**:
   ```bash
   install_dependencies.bat
   ```
   Or manually:
   ```bash
   pip install tkcalendar reportlab pillow opencv-python scikit-learn pandas numpy
   ```

3. **Run the application**:
   ```bash
   python sms.py
   ```

## Default Login Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system access

### Teacher Account (with class assignment)
- **Username:** `j-thomas`
- **Password:** `james`
- **Access:** Assigned to Primary 4 class

### Accountant Account
- **Username:** `accountant1`
- **Password:** `account123`
- **Access:** Financial management, fees, reports

**⚠️ Important:** Change default passwords after first login!

## Usage Guide

### For Administrators
1. Login with admin credentials
2. Access all modules from navigation menu
3. Manage users, classes, students, and teachers
4. Generate comprehensive reports
5. Configure system settings and permissions

### For Teachers
1. Login with teacher credentials
2. View assigned class students only
3. Mark attendance
4. Enter grades
5. Generate class and student reports
6. Use AI insights for early intervention

### For Accountants
1. Login with accountant credentials
2. Manage fee collection
3. Track income and expenses
4. Generate financial reports
5. Monitor arrears and payment patterns

## Database

- **Type:** SQLite3
- **Location:** `database/school_management.db`
- **Backup Location:** `backups/` and `database_backups/`

### Backup Recommendations
- Backup database weekly
- Use built-in backup feature (Admin menu)
- Store backups in secure location
- Test restore procedure periodically

## Key Features Explained

### AI-Powered Insights
The system uses machine learning algorithms to:
- Predict students at risk of poor attendance
- Identify fee payment default risks
- Analyze student performance trends
- Compare individual students to class averages
- Generate behavioral patterns and recommendations

### Responsive Design
- Automatically adjusts to screen resolution
- Optimized for 1366x768 to 1920x1080
- Scrollable interfaces for small screens
- Mobile-friendly dialogs

### Grading System
- Support for multiple assignments per student
- Grade validation (0-100 range)
- Teacher attribution
- Bulk grade viewing and filtering
- Analytics and reporting

### Financial Management
- Income and expense categorization
- Budget planning and tracking
- Transaction history
- Financial report generation
- Multi-category support

## System Requirements

### Minimum
- **OS:** Windows 10 or higher
- **RAM:** 4GB
- **Storage:** 500MB free space
- **Display:** 1280x720 or higher
- **Python:** 3.13+

### Recommended
- **OS:** Windows 11
- **RAM:** 8GB or more
- **Storage:** 1GB free space
- **Display:** 1920x1080 or higher
- **Python:** 3.13.x (latest stable)

## Troubleshooting

### Application won't start
- Ensure Python 3.13 is installed (NOT 3.14 - has Tkinter issues)
- Install all dependencies: `pip install -r requirements.txt`
- Check database file exists in `database/` folder

### AI features not working
- Install optional packages: `pip install scikit-learn pandas numpy`
- Restart the application
- Check AI status in AI Insights menu

### Teacher can't see students
- Admin must create teacher record matching teacher user's full name
- Admin must assign teacher to a class
- Teacher must log out and log back in

### Grades not saving
- Ensure student is selected from dropdown
- Verify grade is between 0-100
- Check database permissions

## File Structure

```
GAYBECK STARKIDS SMS/
├── sms.py                          # Main application
├── requirements.txt                # Python dependencies
├── install_dependencies.bat        # Dependency installer
├── database/
│   └── school_management.db       # Main database
├── backups/                        # Code backups
├── database_backups/              # Database backups
├── teacher_documents/             # Teacher uploaded files
├── docs/                          # Documentation
└── tests/                         # Test scripts
```

## Version History

### Version 2.0.0 (Current)
- ✅ Added grading system with database persistence
- ✅ Implemented AI-powered analytics and insights
- ✅ Added advanced student trend analysis
- ✅ Enhanced teacher-class assignment matching
- ✅ Implemented comprehensive reporting system
- ✅ Added responsive design for all screens
- ✅ Fixed student name extraction in dropdowns
- ✅ Added database backup and restore features

### Version 1.0.0
- Initial release with core functionality

## Support & Maintenance

### Getting Help
- Check documentation in `docs/` folder
- Review user guides and tutorials
- Contact system administrator

### Reporting Issues
- Document the issue with screenshots
- Note any error messages
- Include steps to reproduce
- Check if issue persists after restart

## Security Notes

- 🔐 All users should change default passwords
- 💾 Regular database backups are essential
- 🔒 Limit admin access to authorized personnel
- 📋 Review user permissions regularly
- 🗑️ Remove inactive user accounts

## License

Proprietary - For Gaybeck Starkids School Use Only

## Credits

**Developed for:** Gaybeck Starkids School  
**Development Date:** 2024-2025  
**Technology Stack:** Python, Tkinter, SQLite, scikit-learn

---

**For technical support or feature requests, contact your system administrator.**
