# School Management System - Directory Structure

## 📁 Root Directory Overview

This document describes the organized directory structure of the Gaybeck Starkids SMS application.

```
GAYBECK STARKIDS SMS/
├── .venv/                          # Python virtual environment
├── backups/                        # Application backups
├── database/                       # Database files
│   ├── school_management.db       # Main application database
│   └── school.db                  # Legacy database
├── dev-scripts/                    # Development and maintenance scripts
├── docs/                           # All documentation
├── reports/                        # Generated reports and audit logs
├── scripts/                        # Utility and maintenance scripts
├── teacher_documents/              # Teacher document storage
├── tests/                          # Test files
├── sms.py                         # Main application file
├── requirements.txt               # Python dependencies
├── install_dependencies.bat       # Dependency installer
└── DIRECTORY_STRUCTURE.md         # This file
```

## 📂 Directory Descriptions

### `/database/` - Database Files
Contains all SQLite database files used by the application.
- **school_management.db** - Primary database with all school data
- **school.db** - Legacy database (kept for reference)

### `/docs/` - Documentation
Comprehensive documentation for all features and implementations.

**Key Documents:**
- `APPLICATION_COMPREHENSIVE_REVIEW.md` - Full application review
- `COMPREHENSIVE_OPTIMIZATION_GUIDE.md` - Optimization guide
- `LOGIN_SYSTEM_DOCUMENTATION.md` - Authentication system
- `USER_MANAGEMENT_GUIDE.md` - User management instructions
- `ATTENDANCE_FIX_DOCUMENTATION.md` - Attendance system details
- `ATTENDANCE_REVERSION_SUMMARY.md` - Attendance reversion feature
- `ATTENDANCE_SUBMIT_BUTTON_DOCUMENTATION.md` - Submit button implementation
- `NON_EXPANDABLE_ATTENDANCE_DOCUMENTATION.md` - Attendance display changes
- `DATABASE_TABLE_FIX_DOCUMENTATION.md` - Database schema fixes
- `DATE_PICKER_IMPLEMENTATION_SUMMARY.md` - Date picker integration
- `DATE_PICKER_SCROLLABLE_FORMS_DOCUMENTATION.md` - Enhanced form UX
- `FORM_IMPROVEMENTS_DOCUMENTATION.md` - Form enhancements
- `DYNAMIC_HEADER_IMPLEMENTATION.md` - Dynamic dashboard header
- `COMPREHENSIVE_SYNC_DOCUMENTATION.md` - Data synchronization
- `REAL_TIME_ANALYTICS_DOCUMENTATION.md` - Analytics features
- `EXPORT_AND_USAGE_GUIDE.md` - Export functionality
- `EXECUTIVE_BRIEF.md` - Executive summary
- `STAKEHOLDER_SLIDES_OUTLINE.md` - Presentation materials
- `OPTIMIZATION_SUMMARY_REPORT.md` - Performance optimizations
- `multiple_document_upload_documentation.md` - Document upload feature
- `padding_adjustment_summary.md` - UI padding improvements
- `pil_installation_fix_documentation.md` - PIL/Pillow setup
- `teacher_profile_printing_documentation.md` - Teacher profile printing
- `DIRECTORY_CLEANUP_SUMMARY.md` - Previous cleanup documentation
- `class_management_redesign_documentation.py` - Class management updates
- `teacher_management_redesign_documentation.py` - Teacher management updates
- `style_guide.md` - Application style guidelines
- `APPLICATION_COMPREHENSIVE_REVIEW.html` - HTML review document

### `/scripts/` - Utility Scripts
Maintenance, sync, and utility scripts for database operations.

**Database Maintenance:**
- `check_triggers.py` - Verify database triggers
- `fix_triggers.py` - Fix database trigger issues
- `fix_log_trigger.py` - Fix logging trigger
- `fix_statistics_cache.py` - Fix statistics cache table

**Synchronization Scripts:**
- `sync_fees_to_financial.py` - Sync fees to financial transactions
- `verify_sync.py` - Verify synchronization results
- `comprehensive_sync_system.py` - Comprehensive data sync
- `realtime_sync.py` - Real-time data synchronization
- `incremental_relationships.py` - Incremental relationship updates

### `/dev-scripts/` - Development Scripts
Development tools and fix scripts (mostly legacy/archived).

**Fix Scripts:**
- `aggressive_fix.py`
- `complete_fix.py`
- `comprehensive_fix.py`
- `final_comprehensive_fix.py`
- `final_indentation_fix.py`
- `final_integration.py`
- `fix_application.py`
- `structural_fix.py`
- `ultimate_fix.py`

**Development Tools:**
- `audit_system.py` - System auditing
- `code_optimizer.py` - Code optimization
- `database_manager.py` - Database management utilities
- `database_relationships_sync.py` - Relationship synchronization
- `integration_helper.py` - Integration assistance
- `optimize_database.py` - Database optimization
- `validate_optimizations.py` - Validation tools
- `verify_date_pickers.py` - Date picker verification
- `verify_integration.py` - Integration verification

### `/tests/` - Test Files
Unit tests and feature tests for the application.
- `test_attendance_submit.py` - Attendance submission tests
- `test_dashboard_no_key_stats.py` - Dashboard statistics tests
- `test_dashboard_statistics.py` - Dashboard functionality tests
- `test_header_update.py` - Header update tests
- `test_non_expandable_attendance.py` - Attendance display tests

### `/backups/` - Application Backups
Timestamped backups of the main application file.
- `sms_backup_*.py` - Dated backup files
- `sms_backup.py` - General backup

### `/reports/` - Generated Reports
System-generated reports and audit logs.
- `audit_report_*.txt` - Timestamped audit reports
- `audit_summary.txt` - Audit summary

### `/teacher_documents/` - Teacher Documents
Storage for uploaded teacher documents and files.

### `/.venv/` - Virtual Environment
Python virtual environment with all dependencies installed.

## 🚀 Main Application Files

### `sms.py`
The main School Management System application file containing:
- Login and authentication system
- Student management (registration, profiles, attendance)
- Teacher management (profiles, assignments, documents)
- Class management (creation, assignments, directories)
- Financial management (transactions, categories, budgets, reports)
- Dashboard with real-time statistics
- Comprehensive reporting and analytics

### `requirements.txt`
Python package dependencies:
- tkinter (GUI framework)
- Pillow (Image processing)
- tkcalendar (Date picker widgets)
- reportlab (PDF generation)
- sqlite3 (Database - built-in)

### `install_dependencies.bat`
Windows batch file to automatically install all required Python packages.

## 📊 Database Schema

The `school_management.db` database contains the following main tables:

**Core Tables:**
- `users` - System users and authentication
- `students` - Student information
- `teachers` - Teacher profiles
- `classes` - Class definitions
- `attendance` - Attendance records
- `fees` - Fee payments

**Financial Tables:**
- `financial_transactions` - All financial transactions
- `financial_categories` - Income/expense categories
- `budget_plans` - Budget planning and tracking

**System Tables:**
- `statistics_cache` - Cached statistics for performance
- `teacher_documents` - Teacher document metadata

## 🔧 Maintenance & Usage

### Running the Application
```bash
python sms.py
```

### Installing Dependencies
```bash
# Using batch file (Windows)
install_dependencies.bat

# Or manually
pip install -r requirements.txt
```

### Database Maintenance
```bash
# Check database triggers
python scripts/check_triggers.py

# Sync fees to financial system
python scripts/sync_fees_to_financial.py

# Verify sync results
python scripts/verify_sync.py
```

### Running Tests
```bash
# Run specific tests
python tests/test_attendance_submit.py
python tests/test_dashboard_statistics.py
```

## 📝 Notes

- **Database Location**: All database operations now use `database/school_management.db`
- **Backups**: Automatic backups are stored in the `backups/` directory
- **Documentation**: All documentation centralized in `docs/` for easy access
- **Scripts**: Utility scripts organized by purpose (maintenance, sync, development)
- **Tests**: All test files consolidated in `tests/` directory
- **Clean Root**: Root directory now contains only essential files for better organization

## 🗂️ File Organization Benefits

1. **Easy Navigation**: Related files grouped logically
2. **Better Maintenance**: Clear separation of production, development, and test files
3. **Simplified Backups**: Critical files easily identifiable
4. **Documentation Access**: All docs in one location
5. **Professional Structure**: Industry-standard directory layout
6. **Scalability**: Easy to add new features and components

---

**Last Updated**: November 9, 2025  
**Application Version**: Production  
**Database Version**: school_management.db v2.0
