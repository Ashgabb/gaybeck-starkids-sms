# User Account Testing Guide

## Available User Accounts

All user accounts have been created and verified in the database. Below are the login credentials:

### 1. Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Select "👑 Admin"
- **Permissions**: Full access to all features

### 2. Teacher Account
- **Username**: `teacher`
- **Password**: `teacher123`
- **Role**: Select "👨‍🏫 Teacher"
- **Permissions**: 
  - View assigned class students
  - Mark attendance for assigned class
  - View class reports

### 3. Accountant Account
- **Username**: `accountant`
- **Password**: `accountant123`
- **Role**: Select "💰 Accountant"
- **Permissions**:
  - Fee management
  - Financial transactions
  - Budget management
  - Financial reports

### 4. Staff Account
- **Username**: `staff`
- **Password**: `staff123`
- **Role**: Select "📋 Staff"
- **Permissions**:
  - View student information
  - Limited access to records

## Testing Instructions

### Step 1: Launch Application
```bash
python sms.py
```

### Step 2: Test Each Account

**For Admin:**
1. Enter username: `admin`
2. Enter password: `admin123`
3. Select role: "👑 Admin"
4. Click "🔐 Login"
5. ✓ Should see full dashboard with all features

**For Teacher:**
1. Enter username: `teacher`
2. Enter password: `teacher123`
3. Select role: "👨‍🏫 Teacher"
4. Click "🔐 Login"
5. ✓ Should see dashboard with teacher-specific features

**For Accountant:**
1. Enter username: `accountant`
2. Enter password: `accountant123`
3. Select role: "💰 Accountant"
4. Click "🔐 Login"
5. ✓ Should see dashboard with financial features

**For Staff:**
1. Enter username: `staff`
2. Enter password: `staff123`
3. Select role: "📋 Staff"
4. Click "🔐 Login"
5. ✓ Should see dashboard with limited access

## Common Issues & Solutions

### Issue: "Role Mismatch" Error
**Cause**: Selected role doesn't match the account's assigned role
**Solution**: Make sure to select the correct role radio button that matches the account

### Issue: "Invalid username or password"
**Cause**: Incorrect credentials or account is disabled
**Solution**: 
- Double-check username and password (case-sensitive)
- Verify account is active in database

### Issue: Account not found
**Cause**: User account doesn't exist in database
**Solution**: Run `python tests/check_all_users.py` to create default accounts

## Role Validation

The system enforces role-based access control:
- Each user account has ONE assigned role
- Users MUST select their assigned role when logging in
- Attempting to login with a different role will be rejected
- This ensures proper access control and audit trails

## Database Verification

To verify all accounts exist, run:
```bash
python tests/check_all_users.py
```

This will:
- List all user accounts
- Show their roles and status
- Create missing default accounts if needed
- Display login credentials

## Security Notes

⚠️ **Default Passwords**: These are test credentials. In production:
- Change all default passwords
- Implement password complexity requirements
- Enable password expiration policies
- Use encrypted password storage (currently using plain text for testing)
