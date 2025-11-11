# Settings Module Documentation
## Gaybeck Starkids Academy School Management System

**Date:** 2025-11-10  
**Version:** 2.0.1  
**Module:** Admin Settings Panel

---

## Overview

The Settings module is a comprehensive admin-only control panel that consolidates all system configuration and management features into a single, organized interface with tabbed navigation.

---

## Key Features

### 🎯 Centralized Administration
- All admin functions in one place
- Tabbed interface for easy navigation
- Role-based access control (Admin only)
- Organized by functionality

### 🔒 Security
- Admin-only access
- No visibility for non-admin users
- Permission-based controls
- Confirmation dialogs for destructive operations

---

## Module Structure

### Settings Tabs

The Settings module contains **5 main tabs**:

1. **🗑️ Data Management** - Clear and manage database records
2. **💱 Currency & Finance** - Configure currency and financial categories
3. **👤 User Management** - Manage user accounts (shortcut)
4. **💾 Database** - View and inspect database tables (shortcut)
5. **🔄 Backup & Restore** - Database backup and restore (shortcut)

---

## Tab 1: Data Management

### Purpose
Provides admin tools to clear test data and transition the system from testing to production use.

### Features

#### Clear Operations Available:

1. **Clear All Students**
   - Deletes all student records
   - Automatically cascades to:
     - Attendance records
     - Fee records
     - Grade records
   - Updates class student counts
   - Resets statistics

2. **Clear All Attendance**
   - Removes all attendance records only
   - Preserves student data
   - Useful for new academic year

3. **Clear All Fees**
   - Removes all fee records only
   - Preserves student data
   - Useful for financial year reset

4. **Clear All Grades**
   - Removes all grade records only
   - Preserves student data
   - Useful for new term/semester

5. **Clear All Test Data** (DANGER ZONE)
   - Nuclear option - removes everything except:
     - User accounts
     - Class structure
     - System settings
   - Complete system reset for production

### Safety Features
- ⚠️ Warning banner at top of tab
- Multiple confirmation dialogs
- Color-coded danger zones (red for critical operations)
- Cannot be undone warnings

### Usage Example
```
1. Login as admin
2. Click "⚙️ Settings" in navigation
3. Select "🗑️ Data Management" tab
4. Choose appropriate clear operation
5. Confirm deletion when prompted
6. Data is cleared and statistics updated
```

---

## Tab 2: Currency & Finance

### Purpose
Configure system-wide currency settings and manage financial categories for income and expense tracking.

### Currency Settings

#### Supported Currencies:
- **GHS** - Ghanaian Cedi (Default)
- **USD** - US Dollar
- **EUR** - Euro
- **GBP** - British Pound
- **NGN** - Nigerian Naira
- **ZAR** - South African Rand
- **KES** - Kenyan Shilling
- **UGX** - Ugandan Shilling

#### Features:
- Dropdown selection
- Current currency display
- One-click save
- Stored in `system_settings` table
- Applied system-wide

### Financial Categories Management

#### Income Categories (Default):
1. School Fees
2. Registration Fees
3. Feeding Fees
4. Transportation Fees
5. Extra Curricular Fees
6. Uniform Sales
7. Book Sales
8. Event Fees
9. Donations
10. Other Income

#### Expense Categories (Default):
1. Teacher Salaries
2. Support Staff Salaries
3. Utilities
4. Office Supplies
5. Maintenance & Repairs
6. Transport Expenses
7. Food & Catering
8. Educational Materials
9. Insurance
10. Professional Services
11. Marketing & Advertising
12. Equipment Purchase
13. Training & Development
14. Rent & Leases
15. Other Expenses

#### Category Management Features:
- **Add New Categories**
  - Enter category name
  - Select type (Income/Expense)
  - One-click add
  
- **Delete Categories**
  - Select from list
  - Confirm deletion
  - Prevents accidental deletion

- **Dual List Display**
  - Separate lists for Income and Expense
  - Scrollable lists
  - Easy visibility

### Usage Example
```
Currency Change:
1. Go to Settings > Currency & Finance
2. Select desired currency from dropdown
3. Click "Save Currency"
4. System confirms change

Add Category:
1. Go to Settings > Currency & Finance
2. Scroll to "Add New Category" section
3. Enter category name
4. Select Income or Expense
5. Click "Add Category"
6. Category appears in appropriate list

Delete Category:
1. Select category from Income or Expense list
2. Click "Delete Selected"
3. Confirm deletion
4. Category removed from list
```

---

## Tab 3: User Management

### Purpose
Quick access to the existing User Management interface.

### Features
- Shortcut button to open full User Management
- Maintains existing functionality
- No duplication of code
- Seamless integration

### Access
Click "Open User Management" button to launch the full user management interface in the main content area.

---

## Tab 4: Database Management

### Purpose
Quick access to the existing Database View interface.

### Features
- Shortcut button to open Database View
- Inspect all database tables
- View table schemas
- Export data

### Access
Click "Open Database View" button to launch the database inspection interface.

---

## Tab 5: Backup & Restore

### Purpose
Quick access to the existing Backup & Restore interface.

### Features
- Shortcut button to Backup & Restore
- Create database backups
- Restore from backups
- Backup history

### Access
Click "Open Backup & Restore" button to launch the backup management interface.

---

## Technical Implementation

### Database Schema

#### system_settings Table
```sql
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

**Default Settings:**
| Key | Value | Description |
|-----|-------|-------------|
| currency | GHS | Default system currency |
| school_name | Gaybeck Starkids Academy | School name |
| academic_year | 2024/2025 | Current academic year |

#### financial_categories Table
```sql
CREATE TABLE IF NOT EXISTS financial_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    category_type TEXT NOT NULL CHECK (category_type IN ('income', 'expense', 'Income', 'Expense')),
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_date DATE DEFAULT CURRENT_DATE
)
```

### Key Functions

#### Main Settings Function
```python
def show_settings(self):
    """Admin-only settings panel with tabs for different configurations"""
```
- Creates tabbed interface
- Renders all 5 tabs
- Manages navigation

#### Tab Creation Functions
```python
def create_data_management_tab(self, parent)
def create_currency_finance_tab(self, parent)
def create_user_management_tab(self, parent)
def create_database_management_tab(self, parent)
def create_backup_restore_tab(self, parent)
```

#### Currency Management
```python
def save_currency_setting(self):
    """Save currency setting to database"""
```
- Extracts currency code
- Stores in system_settings
- Confirms to user

#### Category Management
```python
def load_financial_categories(self):
    """Load financial categories from database"""

def add_financial_category(self):
    """Add a new financial category"""

def delete_financial_category(self):
    """Delete selected financial category"""
```

### File Locations

**Main File:** `sms.py`

**Function Locations:**
- Line ~18338: `show_settings()` - Main settings interface
- Line ~18400: `create_data_management_tab()` - Data management tab
- Line ~18465: `create_currency_finance_tab()` - Currency & finance tab
- Line ~18630: `create_user_management_tab()` - User management shortcut
- Line ~18645: `create_database_management_tab()` - Database view shortcut
- Line ~18658: `create_backup_restore_tab()` - Backup & restore shortcut
- Line ~18671: `save_currency_setting()` - Save currency
- Line ~18693: `load_financial_categories()` - Load categories
- Line ~18709: `add_financial_category()` - Add category
- Line ~18730: `delete_financial_category()` - Delete category

**Database Schema:**
- Line ~1934: Financial categories table
- Line ~1944: System settings table

---

## Navigation Changes

### Before
Multiple admin buttons in navigation:
- 👤 User Management
- 🗑️ Data Management
- 💾 Database View
- 🔄 Backup & Restore

### After
Single consolidated button:
- ⚙️ Settings (contains all above + new features)

### Benefits
- Cleaner navigation
- Better organization
- More space for other features
- Logical grouping of admin functions

---

## User Guide

### For Administrators

#### Accessing Settings
1. Login with admin credentials
2. Click "⚙️ Settings" in the navigation menu
3. Select desired tab

#### Changing Currency
1. Settings > Currency & Finance tab
2. Select currency from dropdown
3. Click "Save Currency"
4. System confirms change
5. New currency applies to all financial operations

#### Managing Financial Categories
1. Settings > Currency & Finance tab
2. View current categories in lists
3. To add:
   - Enter name in "Category Name" field
   - Select Income or Expense
   - Click "Add Category"
4. To delete:
   - Click category in list
   - Click "Delete Selected"
   - Confirm deletion

#### Clearing Test Data
1. Settings > Data Management tab
2. Read warning carefully
3. Choose appropriate clear option:
   - Clear specific data type (Students, Attendance, Fees, Grades)
   - Or clear all test data (complete reset)
4. Confirm operation
5. Data is cleared immediately

### For Non-Admin Users
- Settings button is not visible
- Cannot access any admin functions
- System enforces role-based access

---

## Best Practices

### Before Production
1. **Test Thoroughly**
   - Add test students, fees, grades
   - Test all features
   - Verify reports work correctly

2. **Backup Database**
   - Settings > Backup & Restore
   - Create full backup
   - Store securely

3. **Clear Test Data**
   - Settings > Data Management
   - Click "Clear All Test Data"
   - Confirm operation

4. **Set Currency**
   - Settings > Currency & Finance
   - Select appropriate currency
   - Save setting

5. **Configure Categories**
   - Review default categories
   - Add custom categories if needed
   - Remove unused categories

### During Operation
1. **Regular Backups**
   - Weekly minimum
   - Before major changes
   - Store off-site

2. **Category Management**
   - Add categories as needed
   - Don't delete categories with transactions
   - Keep category names clear and descriptive

3. **Currency Changes**
   - Avoid changing mid-year
   - Communicate changes to all users
   - Update fee structures accordingly

---

## Troubleshooting

### Settings Not Visible
**Problem:** Cannot see Settings button  
**Solution:**
- Verify you're logged in as admin
- Check user role in database
- Restart application

### Currency Not Saving
**Problem:** Currency setting doesn't persist  
**Solution:**
- Check database permissions
- Verify system_settings table exists
- Check console for errors

### Categories Not Loading
**Problem:** Category lists are empty  
**Solution:**
- Check database connection
- Run init_database to create defaults
- Verify financial_categories table exists

### Cannot Delete Category
**Problem:** Delete operation fails  
**Solution:**
- Check if category is in use (has transactions)
- Verify database permissions
- Try selecting category again

---

## Future Enhancements

### Potential Additions
- [ ] Academic year management
- [ ] Term/semester settings
- [ ] School information editor
- [ ] Fee structure templates
- [ ] Email configuration
- [ ] SMS gateway settings
- [ ] Report customization
- [ ] Theme settings
- [ ] Language settings
- [ ] Tax settings

---

## Security Considerations

### Access Control
- **Role Check:** Only admin can access Settings
- **Permission Enforcement:** Checked at multiple levels
- **UI Hidden:** Non-admin users don't see Settings button

### Data Protection
- **Confirmation Dialogs:** All destructive operations require confirmation
- **Backup Reminders:** Warnings to backup before clearing data
- **Audit Trail:** Consider logging setting changes

### Best Practices
- Change default admin password immediately
- Limit number of admin accounts
- Regular security audits
- Monitor setting changes

---

## API Reference

### Main Functions

#### show_settings()
```python
def show_settings(self):
    """
    Main settings interface with tabbed navigation.
    Admin-only access.
    Creates 5 tabs for different admin functions.
    """
```

#### save_currency_setting()
```python
def save_currency_setting(self):
    """
    Save selected currency to database.
    Updates system_settings table.
    Shows confirmation message.
    
    Raises:
        Exception: If database update fails
    """
```

#### add_financial_category()
```python
def add_financial_category(self):
    """
    Add new financial category.
    Validates input before adding.
    Refreshes category lists.
    
    Parameters:
        Uses self.new_category_name and self.category_type_var
        
    Raises:
        Exception: If category already exists or database error
    """
```

#### delete_financial_category()
```python
def delete_financial_category(self):
    """
    Delete selected financial category.
    Requires confirmation.
    Updates category lists.
    
    Raises:
        Exception: If category is in use or database error
    """
```

---

## Database Queries

### Get Currency Setting
```sql
SELECT value FROM system_settings WHERE key = 'currency'
```

### Save Currency Setting
```sql
INSERT OR REPLACE INTO system_settings (key, value, updated_date)
VALUES ('currency', ?, CURRENT_TIMESTAMP)
```

### Load Income Categories
```sql
SELECT category_name FROM financial_categories 
WHERE category_type = 'Income' 
ORDER BY category_name
```

### Add Category
```sql
INSERT INTO financial_categories (category_name, category_type)
VALUES (?, ?)
```

### Delete Category
```sql
DELETE FROM financial_categories 
WHERE category_name = ? AND category_type = ?
```

---

## Change Log

### Version 2.0.1 (2025-11-10)
- ✅ Created centralized Settings module
- ✅ Consolidated 4 admin buttons into 1
- ✅ Added Currency Settings tab
- ✅ Added Financial Categories management
- ✅ Created system_settings table
- ✅ Updated financial_categories table schema
- ✅ Implemented currency dropdown with 8 currencies
- ✅ Implemented category add/delete functionality
- ✅ Added default system settings (currency, school name, academic year)
- ✅ Reorganized navigation menu
- ✅ Maintained backward compatibility with existing features

---

## Support

### For Issues
1. Check this documentation
2. Verify admin permissions
3. Check database integrity
4. Review console output for errors
5. Contact system administrator

### For Feature Requests
Document desired functionality and submit to development team.

---

## Conclusion

The Settings module provides a comprehensive, organized interface for all administrative functions in the Gaybeck Starkids Academy School Management System. By consolidating multiple features into a single tabbed interface and adding currency and financial category management, it significantly improves the admin experience and system configurability.

**Key Benefits:**
- ✅ Centralized administration
- ✅ Better navigation organization
- ✅ Currency flexibility
- ✅ Financial category customization
- ✅ Easier data management
- ✅ Professional admin interface

The system is now more flexible, easier to manage, and ready for deployment in various educational contexts with different currencies and financial structures.

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-10  
**Module Version:** 2.0.1  
**Status:** Production Ready
