# School Management System - User Authentication & Role-Based Access Control

## Overview
The School Management System now features a comprehensive login system with role-based permissions to ensure secure access and appropriate functionality for different user types.

## Login System Features

### 🔐 Authentication
- Secure login window with username and password fields
- Database-stored user credentials
- Session management with last login tracking
- Automatic logout functionality
- Protection against unauthorized access

### 👥 User Roles & Permissions

#### 1. **Administrator (admin)**
**Full System Access** - Can manage everything
- ✅ Dashboard (complete overview)
- ✅ Class Management (create, edit, delete classes)
- ✅ Student Management (all students, full CRUD operations)
- ✅ Teacher Management (hire, edit, manage teachers)
- ✅ Fees Management (complete financial control)
- ✅ Attendance Management (all students, all classes)
- ✅ Database View (complete database access)
- ✅ System Configuration
- ✅ User Management (future feature)

#### 2. **Teacher (teacher)**
**Class-Specific Access** - Manages assigned class only
- ✅ Dashboard (overview of their class)
- ✅ Student Management (only students from assigned class)
- ✅ Attendance Management (only their class students)
- ✅ Grade Management (their class students)
- ✅ Class Information (read access)
- ❌ Cannot access other classes' data
- ❌ Cannot manage teachers or system settings
- ❌ Limited fees management

#### 3. **Staff (staff)**
**Limited Access** - Basic operations only
- ✅ Dashboard (basic overview)
- ✅ Student Management (view and limited edit)
- ✅ Attendance Management (view and mark attendance)
- ❌ Cannot manage teachers
- ❌ Cannot access financial data
- ❌ Cannot access database directly

## Default Login Credentials

### Administrator Account
- **Username:** `admin`
- **Password:** `admin123`
- **Full Name:** System Administrator
- **Permissions:** All system features

### Teacher Account
- **Username:** `teacher1` 
- **Password:** `teacher123`
- **Full Name:** Sample Teacher
- **Assigned Class:** Class 3
- **Permissions:** Students, Attendance, Grades for Class 3

### Staff Account
- **Username:** `staff1`
- **Password:** `staff123`
- **Full Name:** Sample Staff
- **Permissions:** Basic student and attendance management

## Security Features

### 🔒 Access Control
- Permission validation on every feature access
- Role-based navigation menu (only shows accessible features)
- Data filtering based on user permissions
- Unauthorized access prevention with error messages

### 👨‍🏫 Teacher-Specific Features
- Teachers can only see students from their assigned class
- Attendance management limited to their class
- Student management restricted to their assigned students
- Class assignment automatically detected from teacher record

### 📊 Permission Feedback
- Clear role display in header section
- Context-aware subtitles showing access level
- Informative error messages for denied access
- User-friendly permission explanations

## Interface Enhancements

### Header Updates
- **User Welcome Message:** Shows current user's full name
- **Role Display:** Shows user role (Admin/Teacher/Staff)
- **Logout Button:** Secure session termination
- **Real-time Date/Time:** System status information

### Navigation Updates
- **Permission-Aware Menu:** Only shows accessible features
- **Role-Based Buttons:** Dynamic button visibility
- **Context Hints:** Feature descriptions based on role

### Content Adaptations
- **Filtered Data Views:** Teachers see only their class data
- **Role-Specific Subtitles:** Context-aware descriptions
- **Permission Validation:** Real-time access checking

## Database Schema Updates

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',
    email TEXT,
    phone TEXT,
    permissions TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_date DATE DEFAULT CURRENT_DATE,
    last_login DATE
);
```

### Teacher-Class Relationship
- Teachers table includes `class_id` for assignment
- System automatically detects teacher's assigned class
- Permission filtering based on class assignment

## Usage Instructions

### 1. Starting the Application
```bash
python sms.py
```
- Login window appears automatically
- Main application hidden until successful login

### 2. Logging In
1. Enter username and password
2. Click "LOGIN" button or press Enter
3. System validates credentials and role
4. Main application opens with appropriate permissions

### 3. Role-Based Operations
- **Admin:** Access all features without restrictions
- **Teacher:** Manage only assigned class students
- **Staff:** Basic operations with limited access

### 4. Logging Out
- Click "Logout" button in header
- Confirm logout in dialog
- Return to login screen

## Security Considerations

### Password Management
- Default passwords should be changed immediately
- Consider implementing password complexity requirements
- Future: Add password reset functionality

### Session Management
- Sessions terminate on logout
- Login tracking for audit purposes
- Automatic session timeout (future enhancement)

### Data Protection
- Role-based data filtering prevents unauthorized access
- Permission validation on all operations
- Clear audit trail of user actions

## Future Enhancements

### Planned Features
- [ ] Password change functionality
- [ ] User profile management
- [ ] Advanced permission granularity
- [ ] Session timeout management
- [ ] User activity logging
- [ ] Password recovery system
- [ ] Multi-factor authentication
- [ ] Role hierarchy management

### Administration Features
- [ ] User management interface for admins
- [ ] Dynamic role assignment
- [ ] Permission customization
- [ ] User activity reports
- [ ] Security audit logs

## Troubleshooting

### Common Issues
1. **Login Failed:** Check username/password spelling
2. **Access Denied:** Contact administrator for permission issues
3. **No Class Assigned:** Teachers need class assignment in database
4. **Feature Not Visible:** Check user role permissions

### Database Issues
- Ensure `school_management.db` exists and is accessible
- Check database permissions and file locks
- Verify user records in database

## Technical Implementation

### Permission System
- Role-based access control (RBAC)
- Dynamic permission checking
- Graceful error handling for denied access

### User Interface Adaptations
- Context-sensitive navigation
- Role-aware content filtering
- Permission-based feature visibility

### Database Integration
- Secure credential storage
- Efficient permission queries
- Optimized data filtering

---

**Note:** This authentication system provides a solid foundation for school management security. Administrators should change default passwords and configure user accounts according to their institution's requirements.