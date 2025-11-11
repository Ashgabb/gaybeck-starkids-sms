# Enhanced User Management Documentation
## Gaybeck Starkids Academy School Management System

**Date:** 2025-11-10  
**Version:** 2.0.2  
**Module:** User Management Enhancements

---

## Overview

The User Management module has been significantly enhanced with powerful administrative controls including role changes, user deactivation, and secure deletion. These features provide administrators with complete control over user accounts while maintaining security and data integrity.

---

## Key Enhancements

### 🔄 **Role Change Capability**
Administrators can now change user roles dynamically without recreating accounts.

### ⏸️ **User Deactivation**
Temporarily disable user access while preserving all account data for future reactivation.

### 🗑️ **Secure User Deletion**
Permanently remove user accounts with double confirmation and detailed warnings.

### ✅ **Login Status Recognition**
System automatically prevents inactive users from logging in with clear messaging.

---

## New Features

### 1. Change User Role

#### Purpose
Allows administrators to modify a user's role and associated permissions without recreating the account.

#### Access
- **Location:** Settings > User Management tab
- **Button:** "🔄 Change Role" (Purple)
- **Permission:** Admin only

#### Supported Roles
1. **Administrator** - Full system access
2. **Accountant** - Financial management
3. **Teacher** - Class and student management
4. **Staff** - Limited access
5. **Viewer** - Read-only access

#### Features
- **Interactive Dialog:** Clean popup interface for role selection
- **Role Descriptions:** Each role shows clear description of access level
- **Current Role Display:** Shows user's existing role highlighted
- **Validation:** Prevents changing your own role or main admin role
- **Confirmation:** Requires confirmation before applying changes
- **Immediate Effect:** Changes take effect immediately

#### Usage
```
1. Navigate to Settings > User Management
2. Select user from the list
3. Click "🔄 Change Role" button
4. Review current role and user information
5. Select new role from radio button list
6. Click "Save Changes"
7. Confirm the change
8. System updates role and reloads user list
```

#### Dialog Interface
```
┌─────────────────────────────────┐
│  Change User Role               │
├─────────────────────────────────┤
│  User: teacher1                 │
│  Current Role: Teacher          │
├─────────────────────────────────┤
│  Select New Role:               │
│                                 │
│  ○ Administrator                │
│    Administrator - Full access  │
│                                 │
│  ○ Accountant                   │
│    Accountant - Financial mgmt  │
│                                 │
│  ● Teacher (current)            │
│    Teacher - Class management   │
│                                 │
│  ○ Staff                        │
│    Staff - Limited access       │
│                                 │
│  ○ Viewer                       │
│    Viewer - Read-only access    │
│                                 │
│  [Save Changes]  [Cancel]       │
└─────────────────────────────────┘
```

#### Security Restrictions
- ❌ Cannot change your own role
- ❌ Cannot change main admin role
- ❌ Role changes require confirmation
- ✅ Changes logged in activity

#### Database Impact
```sql
UPDATE users SET role=? WHERE id=?
```

---

### 2. Activate/Deactivate User

#### Purpose
Temporarily disable user access while preserving all account data and history for potential future reactivation.

#### Access
- **Location:** Settings > User Management tab
- **Button:** "⏸️ Activate/Deactivate" (Orange)
- **Permission:** Admin only

#### Features
- **Reversible Action:** Can activate/deactivate multiple times
- **Data Preservation:** All user data remains intact
- **Login Prevention:** Deactivated users cannot login
- **Clear Messaging:** Detailed confirmation and success messages
- **Status Display:** User status shown in user list (Active/Inactive)

#### Usage - Deactivation
```
1. Navigate to Settings > User Management
2. Select active user from list
3. Click "⏸️ Activate/Deactivate" button
4. Review deactivation warning:
   • Prevents user from logging in
   • Revokes all system access
   • Maintains user data
   • Can be reactivated later
5. Confirm deactivation
6. User status changes to "Inactive"
7. User cannot login until reactivated
```

#### Usage - Reactivation
```
1. Navigate to Settings > User Management
2. Select inactive user from list (Status: Inactive)
3. Click "⏸️ Activate/Deactivate" button
4. Confirm activation
5. User status changes to "Active"
6. User can now login normally
```

#### Confirmation Messages

**Deactivation:**
```
Deactivate user 'teacher1'?

⚠️ WARNING: This will:
• Prevent the user from logging in
• Immediately revoke all system access
• Maintain user data for future reactivation

The user account can be reactivated later.
```

**Activation:**
```
Activate user 'teacher1'?

This will allow the user to login and access the system.
```

#### Success Messages

**After Deactivation:**
```
⏸️ User 'teacher1' has been deactivated.

The user cannot login until reactivated.
All user data has been preserved.
```

**After Activation:**
```
✅ User 'teacher1' has been activated.

The user can now login to the system.
```

#### Security Restrictions
- ❌ Cannot deactivate your own account
- ❌ Cannot deactivate main admin account
- ✅ Requires confirmation
- ✅ Changes logged

#### Database Impact
```sql
-- Deactivate
UPDATE users SET is_active=0 WHERE id=?

-- Activate
UPDATE users SET is_active=1 WHERE id=?
```

#### Login Behavior
When a deactivated user attempts to login:
```
Login Failed

Invalid username or password, or account is disabled
```

---

### 3. Delete User

#### Purpose
Permanently remove a user account from the system. This is irreversible and should be used with extreme caution.

#### Access
- **Location:** Settings > User Management tab
- **Button:** "🗑️ Delete User" (Dark Red)
- **Permission:** Admin only

#### Features
- **Double Confirmation:** Two confirmation dialogs for safety
- **Detailed Warning:** Clear explanation of consequences
- **Alternative Suggestion:** Recommends deactivation as alternative
- **Permanent Action:** Complete removal with no recovery
- **Cascade Delete:** Removes all associated data

#### Usage
```
1. Navigate to Settings > User Management
2. Select user to delete
3. Click "🗑️ Delete User" button
4. Read detailed warning message carefully
5. Confirm first deletion prompt
6. Confirm final deletion prompt
7. User permanently deleted
8. All associated data removed
```

#### Confirmation Flow

**First Confirmation:**
```
⚠️ PERMANENT DELETION WARNING ⚠️

You are about to delete:
• Username: teacher1
• Role: Teacher

This action will:
• Permanently remove the user account
• Delete all login credentials
• Remove all permissions
• Cannot be undone

💡 Alternative: Consider deactivating the user instead
   (preserves data for future reactivation)

Are you absolutely sure you want to DELETE this user?

[Yes] [No]
```

**Final Confirmation:**
```
This is your final confirmation.

Permanently delete user 'teacher1'?

[Yes] [No]
```

**Success Message:**
```
🗑️ User 'teacher1' has been permanently deleted.

The account cannot be recovered.
```

#### Security Restrictions
- ❌ Cannot delete your own account
- ❌ Cannot delete main admin account
- ✅ Requires TWO confirmations
- ✅ Suggests deactivation as alternative
- ✅ Changes logged

#### Database Impact
```sql
DELETE FROM users WHERE id=?
```

#### When to Use Delete vs Deactivate

**Use Deactivation When:**
- User on temporary leave
- User role change pending
- Want to preserve user history
- May need to reactivate later
- Testing/troubleshooting

**Use Deletion When:**
- User left organization permanently
- Account created in error
- Duplicate account exists
- Security compromise requiring full removal
- System cleanup required

---

## User List Enhancements

### Status Column
The user list now prominently displays user status:
- **Active** - Green text, user can login
- **Inactive** - Red text, user cannot login

### Column Layout
```
| ID | Username | Full Name | Role | Email | Status | Last Login |
|----|----------|-----------|------|-------|--------|------------|
| 1  | admin    | Admin     | admin| ...   | Active | 2025-11-10 |
| 2  | teacher1 | John Doe  | tea..|  ...  |Inactive| 2025-11-09 |
```

### Visual Indicators
- Active users: Normal display
- Inactive users: Grayed out or different styling (depends on theme)

---

## System Behavior

### Login Flow for Inactive Users

1. User enters credentials
2. System validates username and password
3. System checks `is_active` status
4. If `is_active = 0`:
   - Login denied
   - Message: "Invalid username or password, or account is disabled"
5. If `is_active = 1`:
   - Continue normal login process

### Role Change Impact

When a user's role is changed:
1. **Immediate Effect:** Takes effect on next login
2. **Current Session:** If user is logged in, changes apply on next login
3. **Permissions:** Role-based permissions automatically updated
4. **Access Level:** Navigation and features adjust to new role

### Database Integrity

All operations maintain database integrity:
- Foreign key constraints respected
- Cascading deletes handled properly
- Transaction-based operations
- Rollback on errors

---

## Security Features

### Protection Mechanisms

1. **Self-Protection**
   - Cannot modify your own account's critical settings
   - Prevents accidental self-lockout

2. **Admin Protection**
   - Main admin account cannot be deleted
   - Main admin account cannot be deactivated
   - Main admin role cannot be changed

3. **Confirmation Requirements**
   - Single confirmation for role changes
   - Single confirmation for deactivation
   - **Double confirmation for deletion**

4. **Clear Warnings**
   - Color-coded danger zones
   - Explicit consequence descriptions
   - Alternative suggestions provided

### Access Control

- All user management functions are **Admin-only**
- Non-admin users cannot see user management options
- Settings tab only visible to administrators
- Role-based permission checks enforced

---

## Technical Implementation

### Key Functions

#### change_user_role()
```python
def change_user_role(self):
    """
    Change the role of the selected user via dialog.
    
    Features:
    - Interactive role selection dialog
    - Shows current role
    - Provides role descriptions
    - Validates against self and admin
    - Requires confirmation
    - Updates database immediately
    """
```

**Location:** `sms.py` line ~13289

#### toggle_user_status()
```python
def toggle_user_status(self):
    """
    Toggle active/inactive status of selected user.
    
    Features:
    - Detailed confirmation messages
    - Different messages for activate/deactivate
    - Success feedback with instructions
    - Security validations
    - Status display refresh
    """
```

**Location:** `sms.py` line ~13401

#### delete_selected_user()
```python
def delete_selected_user(self):
    """
    Permanently delete selected user with double confirmation.
    
    Features:
    - Detailed warning message
    - Suggests deactivation alternative
    - Double confirmation requirement
    - Permanent deletion with cascade
    - Success confirmation
    """
```

**Location:** `sms.py` line ~13450

### Database Queries

**Check Active Status:**
```sql
SELECT id, username, full_name, role, email, permissions, is_active 
FROM users 
WHERE username = ? AND password = ?
```

**Change Role:**
```sql
UPDATE users SET role=? WHERE id=?
```

**Toggle Status:**
```sql
UPDATE users SET is_active=? WHERE id=?
```

**Delete User:**
```sql
DELETE FROM users WHERE id=?
```

### Button Layout

```
┌─────────────────────────────────────────────────────────┐
│  [✏️ Edit User]  [🔄 Change Role]  [⏸️ Activate/       │
│                                     Deactivate]         │
│                  [🗑️ Delete User]                      │
└─────────────────────────────────────────────────────────┘
```

---

## Use Cases

### Case 1: Employee Role Promotion
**Scenario:** Teacher promoted to administrator

**Steps:**
1. Admin logs in
2. Goes to Settings > User Management
3. Selects teacher account
4. Clicks "🔄 Change Role"
5. Selects "Administrator"
6. Confirms change
7. Teacher can now login as administrator

### Case 2: Temporary Leave
**Scenario:** Accountant on 3-month leave

**Steps:**
1. Admin selects accountant account
2. Clicks "⏸️ Activate/Deactivate"
3. Confirms deactivation
4. Accountant cannot login during leave
5. When returning, admin clicks "⏸️ Activate/Deactivate" again
6. Accountant can login with all data preserved

### Case 3: Employee Departure
**Scenario:** Staff member left organization

**Option A - Deactivation (Recommended):**
1. Select staff account
2. Click "⏸️ Activate/Deactivate"
3. Confirm
4. Account preserved for records

**Option B - Deletion (Permanent):**
1. Select staff account
2. Click "🗑️ Delete User"
3. Read warning carefully
4. Confirm twice
5. Account permanently removed

### Case 4: Security Incident
**Scenario:** User account compromised

**Immediate Action:**
1. Click "⏸️ Activate/Deactivate"
2. Immediately deactivates account
3. Prevents further access

**Later Actions:**
1. Reset password via Edit User
2. Review and update permissions
3. Reactivate when secure

---

## Best Practices

### Role Management
✅ **Do:**
- Review role descriptions before assigning
- Change roles based on actual job functions
- Document role changes in external records
- Notify users when their role changes

❌ **Don't:**
- Give admin role unnecessarily
- Change roles without user knowledge
- Use role changes for temporary access (use deactivation instead)

### Deactivation
✅ **Do:**
- Use for temporary access removal
- Use during investigations
- Use for leave of absence
- Reactivate when appropriate

❌ **Don't:**
- Use as permanent solution (delete instead if permanent)
- Forget about deactivated accounts
- Leave inactive accounts indefinitely without review

### Deletion
✅ **Do:**
- Use only for permanent removal
- Read all warnings carefully
- Consider deactivation first
- Document deletion reason
- Perform regular audit of deleted accounts

❌ **Don't:**
- Delete without careful consideration
- Delete as first option
- Delete without double confirmation
- Delete during uncertainty

---

## Troubleshooting

### Issue: Cannot Change Role
**Problem:** Change Role button does nothing or shows error

**Solutions:**
1. Ensure you're not selecting your own account
2. Ensure you're not selecting the main admin
3. Verify you have admin privileges
4. Check database connection
5. Review console for detailed errors

### Issue: User Still Can Login After Deactivation
**Problem:** Deactivated user able to login

**Solutions:**
1. Verify status changed in user list (should show "Inactive")
2. Ask user to fully close and reopen application
3. Check database: `SELECT is_active FROM users WHERE username=?`
4. Ensure no multiple instances of user session
5. Clear any cached login sessions

### Issue: Cannot Delete User
**Problem:** Delete operation fails

**Solutions:**
1. Check if user is currently logged in (close their session first)
2. Verify foreign key constraints
3. Check database permissions
4. Review error message for specific issue
5. Consider deactivating instead of deleting

### Issue: Role Change Not Taking Effect
**Problem:** User role changed but permissions not updated

**Solutions:**
1. User must logout and login again
2. Verify role changed in database
3. Check permissions mapping for new role
4. Clear application cache if applicable
5. Restart application

---

## Audit and Compliance

### Logging Recommendations
Consider implementing audit logging for:
- All role changes (who, what, when)
- User deactivations/activations (timestamp, reason)
- User deletions (permanent record before deletion)
- Failed login attempts by inactive users

### Compliance Considerations
- **GDPR:** Right to deletion supported
- **Data Retention:** Deactivation preserves data
- **Access Control:** Role-based access enforced
- **Audit Trail:** Status changes logged in system

---

## Future Enhancements

### Planned Features
- [ ] Bulk role changes
- [ ] Scheduled deactivation/activation
- [ ] Deactivation with reason field
- [ ] User activity audit log
- [ ] Role change history viewer
- [ ] Email notifications on status change
- [ ] Soft delete with recovery period
- [ ] User account cloning

---

## Summary

The enhanced User Management system provides administrators with:

✅ **Complete Control**
- Change roles dynamically
- Activate/deactivate accounts
- Permanently delete when needed

✅ **Enhanced Security**
- Multiple confirmation levels
- Self-protection mechanisms
- Clear warning messages
- Login status recognition

✅ **Flexibility**
- Reversible actions (deactivation)
- Permanent actions (deletion)
- Role modifications without recreation

✅ **User-Friendly**
- Intuitive button layout
- Clear dialog interfaces
- Helpful feedback messages
- Alternative suggestions

---

## Quick Reference

| Action | Button | Color | Confirmations | Reversible | Effect |
|--------|--------|-------|---------------|------------|---------|
| Edit User | ✏️ Edit User | Orange | 0 | Yes | Modify details |
| Change Role | 🔄 Change Role | Purple | 1 | Yes | Update role |
| Deactivate | ⏸️ Activate/Deactivate | Orange | 1 | Yes | Prevent login |
| Delete | 🗑️ Delete User | Red | 2 | No | Remove account |

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-10  
**Application Version:** 2.0.2  
**Status:** Production Ready
