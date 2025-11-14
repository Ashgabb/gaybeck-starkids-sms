# School Management System - User Management Guide

## Overview
The School Management System now includes comprehensive role-based access control with user management capabilities. Only administrators have access to all modules and can create/manage user accounts.

## User Roles and Permissions

### Administrator (admin)
- **UNLIMITED ACCESS**: Has unrestricted access to ALL modules, features, and system functions
- **No Restrictions**: Bypasses all permission checks and security restrictions
- **User Management**: Can create, edit, activate/deactivate, and delete user accounts
- **System Management**: Full access to database views and all system settings
- **Override Authority**: Can access any feature regardless of configured permissions
- **Default Account**: username: `admin`, password: `admin123`

### Teacher (teacher)
- **NO DEFAULT ACCESS**: Teacher accounts start with zero permissions
- **Admin Must Assign**: Only administrators can grant specific permissions
- **Typical Permissions** (when granted by admin):
  - Dashboard access
  - Student Management
  - Attendance Management
  - Class Management
- **Sample Account**: username: `teacher1`, password: `teacher123` (NO PERMISSIONS by default)

### Staff (staff)
- **NO DEFAULT ACCESS**: Staff accounts start with zero permissions
- **Admin Must Assign**: Only administrators can grant specific permissions
- **Typical Permissions** (when granted by admin):
  - Dashboard access
  - Student Management (limited)
  - Attendance Management
- **Sample Account**: username: `staff1`, password: `staff123` (NO PERMISSIONS by default)

### Viewer (viewer)
- **NO DEFAULT ACCESS**: Viewer accounts start with zero permissions
- **Admin Must Assign**: Even viewers need explicit permission grants
- **Typical Permissions** (when granted by admin):
  - Dashboard access (read-only)

## User Management Features (Admin Only)

### Accessing User Management
1. Login as an administrator
2. Navigate to "👤 User Management" in the sidebar
3. The interface includes two tabs:
   - **Users List**: View and manage existing users
   - **Add/Edit User**: Create new users or modify existing ones

### Creating New Users
1. Go to the "📝 Add/Edit User" tab
2. Fill in the required fields:
   - **Username**: Unique username for login
   - **Full Name**: Display name for the user
   - **Email**: User's email address
   - **Password**: Login password (required for new users)
   - **Role**: Select from admin, teacher, staff, or viewer
   - **Status**: Active or Inactive
   - **Permissions**: Select specific permissions (auto-set for admin role)

3. Click "💾 Save User" to create the account

### Managing Existing Users
- **Search**: Use the search box to find users by username, name, email, or role
- **Edit**: Double-click a user or select and click "✏️ Edit User"
- **Toggle Status**: Select a user and click "🔄 Toggle Status" to activate/deactivate
- **Delete**: Select a user and click "🗑️ Delete User" (cannot delete self or main admin)

### Permission System
- **Admin**: Automatically gets all permissions (cannot be restricted)
- **All Other Users**: Start with ZERO permissions by default
- **Permission Assignment**: Only admins can grant specific permissions
- **Available Permissions**:
  - Dashboard Access
  - Student Management
  - Teacher Management
  - Class Management
  - Attendance Tracking
  - Fees Management
  - User Management
  - Database View
- **Permission Templates**: Quick assignment for common roles (Teacher, Staff, Viewer)

## Security Features

### Access Control
- **Admin users have UNLIMITED ACCESS** - no restrictions apply
- Non-admin users can only access modules they have permission for
- Unauthorized access attempts show error messages for non-admin users
- Admin-only modules are hidden from non-admin users but always visible to admin

### Account Protection
- Users cannot delete or disable their own accounts
- The main admin account cannot be deleted or disabled
- Password changes require the new password to be entered

### Login Security
- Failed login attempts show appropriate error messages
- Inactive accounts cannot log in
- Session management ensures only one user session at a time

## Best Practices

### For Administrators
1. **Regular Review**: Regularly review user accounts and permissions
2. **Strong Passwords**: Enforce strong passwords for all accounts
3. **Least Privilege**: Give users only the minimum permissions they need
4. **Account Cleanup**: Deactivate accounts for users who no longer need access

### For All Users
1. **Password Security**: Use strong, unique passwords
2. **Logout**: Always logout when finished using the system
3. **Report Issues**: Report any access problems to administrators

## Troubleshooting

### Common Issues
1. **Cannot Access Module**: Check with admin about your role and permissions
2. **Login Failed**: Verify username/password and account status
3. **Permission Denied**: Contact administrator to request additional permissions

### Admin Issues
1. **Cannot Delete User**: Check if trying to delete self or main admin
2. **User Not Found**: Refresh the user list and try again
3. **Database Errors**: Check database connectivity and permissions

## Login Process with Role Selection

### Step 1: Enter Credentials
- Enter your **username** and **password**

### Step 2: Select Role
Choose your role from the available options:
- **👑 Administrator**: Full system access (requires admin account)
- **👨‍🏫 Teacher**: Teacher-level access
- **👥 Staff Member**: Staff-level access  
- **👁️ Viewer**: Read-only access

### Step 3: Role Validation
- **Administrator role**: Only accounts with admin privileges can select this
- **Other roles**: Any user can select these, but permissions are still controlled by admin

## Default Accounts

| Username | Password | Account Type | Can Login As |
|----------|----------|--------------|---------------|
| admin | admin123 | Administrator | 👑 Administrator (unlimited access) |
| teacher1 | teacher123 | Teacher | 👨‍🏫 Teacher, 👥 Staff, 👁️ Viewer |
| staff1 | staff123 | Staff | 👨‍🏫 Teacher, 👥 Staff, 👁️ Viewer |

**Important**: 
- Change default passwords immediately after first login
- Role selection affects UI and available modules
- Actual permissions are still controlled by admin assignments

## Benefits of Role Selection at Login

### 🎯 **Flexible Access Control**
- Users can choose appropriate role based on their current task
- Same account can be used for different access levels
- Prevents need for multiple accounts per user

### 🔒 **Enhanced Security**
- Administrator role protected - only admin accounts can select it
- Role selection creates audit trail of user intentions
- Helps prevent accidental high-privilege access

### 👥 **Multi-Role Support**
- Teachers can login as staff for limited tasks
- Staff can login as viewers for read-only access
- Flexible workflow based on job requirements

### 📊 **Better User Experience**
- Clear visual indication of selected role
- Intuitive role icons and descriptions
- Simplified access based on current needs

## Module Access Matrix

| Module | Admin | Teacher* | Staff* | Viewer* |
|--------|-------|----------|--------|---------|
| Dashboard | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| Class Management | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| Student Management | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| Teacher Management | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| Fees Management | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| Attendance | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |
| User Management | ✅ Always | ❌ Never** | ❌ Never** | ❌ Never** |
| Database View | ✅ Always | ❌ Must be granted | ❌ Must be granted | ❌ Must be granted |

*All non-admin users start with ZERO permissions
**User Management is admin-only and cannot be granted to other roles

## Support
For technical support or questions about user management, contact your system administrator.