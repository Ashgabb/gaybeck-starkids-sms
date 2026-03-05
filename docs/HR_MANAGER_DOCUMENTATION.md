# HR Manager Module - Documentation

## Overview

The HR Manager module is a comprehensive employee management system integrated into the Gaybeck Starkids School Management System. It provides tools for managing employee timesheets, attendance, payslip generation, AI-powered performance analysis, and training program recommendations.

### Version
- **Module Version**: 1.0.0
- **Integration Date**: March 2026
- **Last Updated**: March 5, 2026

---

## Features

### 1. **Employee Management**
- Add, edit, and delete employee records
- Store employee details (name, position, department, salary, contact info)
- Track hire dates and employment status
- Automatic performance score calculation

### 2. **Timesheet Tracking**
- Record daily hours worked
- Track overtime hours
- Monitor leave hours
- Monthly timesheet summaries
- Automated calculation for payroll integration

### 3. **Attendance Management**
- Mark employee attendance (Present/Absent/Leave/Late)
- Track attendance trends over time
- Generate attendance reports by month/year
- Integration with performance scoring

### 4. **Payslip Generation**
- Automatic payslip calculation based on timesheets
- Support for deductions and allowances
- PDF payslip generation
- Monthly payroll processing
- Gross and net pay calculation

### 5. **AI-Powered Analytics**
- **Performance Scoring**: Automated calculation (0-100) based on:
  - Attendance rate (30% weight)
  - Performance ratings (40% weight)
  - Hours worked vs. expected (30% weight)

- **Training Needs Identification**: Smart detection of:
  - Performance gaps by skill area
  - Attendance issues
  - Professional development needs

- **Recommended Actions**: Automatic suggestions for:
  - Recognition & incentives (for high performers)
  - Performance improvement plans (for low performers)
  - Performance monitoring (for medium performers)
  - Attendance warnings (when needed)

### 6. **Training Program Management**
- Create and manage training programs
- Assign employees to training
- Track training completion and certification
- Link training to performance improvement needs

---

## Database Schema

### Core Tables

#### `employees`
Stores basic employee information
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT UNIQUE)
- position (TEXT)
- department (TEXT)
- salary (REAL)
- email (TEXT UNIQUE)
- phone (TEXT)
- hire_date (TEXT)
- status (TEXT: Active/Inactive/On Leave)
- created_at, updated_at (TIMESTAMPS)
```

#### `timesheets`
Records monthly timesheet entries
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- month, year (INTEGER)
- hours_worked (REAL)
- overtime_hours (REAL)
- leave_hours (REAL)
- notes (TEXT)
- UNIQUE(employee_id, month, year)
```

#### `employee_attendance`
Daily attendance records
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- date (TEXT)
- present (INTEGER: 0/1)
- status (TEXT: Present/Absent/Leave/Late)
- notes (TEXT)
- UNIQUE(employee_id, date)
```

#### `payslips`
Generated payslip records
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- month, year (INTEGER)
- basic_pay, overtime_pay, allowances (REAL)
- gross_pay, deductions, net_pay (REAL)
- status (TEXT: Draft/Processed/Paid)
- payment_date (TEXT)
```

#### `payroll_deductions`
Individual deduction records
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- month, year (INTEGER)
- deduction_type (TEXT)
- amount (REAL)
- description (TEXT)
```

#### `payroll_allowances`
Individual allowance records
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- month, year (INTEGER)
- allowance_type (TEXT)
- amount (REAL)
- description (TEXT)
```

#### `employee_assessments`
Performance assessment records
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- assessment_type (TEXT)
- performance_rating (REAL: 0-5)
- comments (TEXT)
- assessor_id (INTEGER)
- date (TEXT)
```

#### `training_programs`
Available training programs
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT UNIQUE)
- description (TEXT)
- category (TEXT)
- duration_days (INTEGER)
- cost (REAL)
- provider (TEXT)
- status (TEXT: Active/Inactive/Completed)
```

#### `employee_training`
Employee training enrollment
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- training_id (FOREIGN KEY)
- start_date, end_date (TEXT)
- status (TEXT: Scheduled/In Progress/Completed/Cancelled)
- completion_score (REAL: 0-100)
- certification_date (TEXT)
```

#### `hr_actions`
Recommended HR actions tracked
```sql
- id (INTEGER PRIMARY KEY)
- employee_id (FOREIGN KEY)
- action_type (TEXT)
- description (TEXT)
- urgency (TEXT: Low/Medium/High)
- due_date (TEXT)
- status (TEXT: Open/In Progress/Completed/Closed)
- assigned_to (TEXT)
```

---

## Installation & Setup

### Step 1: Initialize Database Tables

Run the initialization script to create all HR-related tables:

```bash
python initialize_hr_database.py
```

This will:
- Create all HR tables
- Set up foreign key relationships
- Create indexes for performance
- Establish update triggers for timestamps

### Step 2: Verify Installation

The script will display:
- ✓ Confirmation of each table created
- ✓ Index creation confirmation
- ✓ Trigger creation confirmation
- ✅ Overall completion status

If any errors occur, check the database file path and ensure the database directory exists.

### Step 3: Launch HR Manager

The HR Manager is accessible from the main application:

1. Open School Management System (`python sms.py`)
2. Log in as Admin or authorized user
3. In the navigation sidebar, click "👔 HR Manager"
4. The HR Manager window will open with all tabs

---

## Usage Guide

### Employee Management Tab

#### Adding an Employee
1. Click "➕ Add Employee" button
2. Fill in all employee details:
   - Name (unique)
   - Position
   - Department
   - Annual Salary
   - Email (optional)
   - Phone (optional)
3. Click "Save"
4. Employee will appear in the employee list

#### Viewing Employee Details
1. Select an employee from the list
2. Details appear in the right panel:
   - Basic information
   - Performance score
   - Recent activities

#### Editing/Deleting
- Select employee and use Edit/Delete buttons
- Confirm actions when prompted

### Timesheet Tab

#### Recording Timesheets
1. Select employee from dropdown
2. Choose month/year
3. Load existing timesheet or create new
4. Enter daily hours:
   - Hours Worked
   - Overtime Hours
   - Leave Hours
5. Save changes

#### Monthly Summary
- View total hours worked vs. expected (160)
- Identify overtime accumulation
- Track leave usage

### Attendance Tab

#### Mark Attendance
1. Select employee and date
2. Choose status:
   - ✓ Present
   - ✗ Absent
   - ✋ Leave
   - ⏰ Late
3. Add notes if needed
4. Save record

#### Attendance Patterns
- System tracks attendance automatically
- Generates monthly reports
- Integrated with performance scoring

### Payslips Tab

#### Preview Payslip
1. Select employee
2. Choose month/year
3. Click "Preview Payslip"
4. Review breakdown:
   - Basic Pay
   - Overtime Pay
   - Allowances
   - Deductions
   - Net Pay

#### Generate PDF
1. Preview payslip (above steps)
2. Click "Generate PDF"
3. Choose save location
4. PDF created with formatted layout

#### Payslip Calculation
```
Basic Pay = (Salary / 160) × Hours Worked
Overtime Pay = Overtime Hours × (Hourly Rate × 1.5)
Gross Pay = Basic + Overtime + Allowances
Net Pay = Gross - Deductions
```

### Performance & Training Tab

#### View Employee Performance
1. Select employee from dropdown
2. System displays:
   - **Performance Score** (0-100)
   - **Training Needs** (with priority levels)
   - **Recommended Actions** (with due dates)

#### Performance Score Interpretation
- **80-100**: Excellent performer
  - Actions: Recognition, incentives, advanced training
- **60-79**: Satisfactory performer
  - Actions: Regular monitoring, skill development
- **0-59**: Below expectations
  - Actions: Improvement plan, intensive training

#### Training Recommendations
The system automatically identifies training needs based on:
- Performance gaps in specific areas
- Attendance issues
- Skill assessments
- Department requirements

### AI Insights Tab

#### Overall Performance Analysis
1. Click "🎯 Overall Performance Analysis"
2. View metrics:
   - High performers percentage
   - Medium performers percentage
   - Low performers percentage
3. View AI-generated recommendations

#### Department Analytics
1. Click "📊 Department Analytics"
2. View by department:
   - Average performance scores
   - Training needs by area
   - Staffing efficiency metrics

---

## AI Analytics Engine

### Performance Scoring Algorithm

```
Score = (Attendance × 0.3) + (Performance Rating × 0.4) + (Hours × 0.3)

Where:
- Attendance: % of days present / total days (last 90 days)
- Performance Rating: Average assessment rating × 20 (to scale 0-100)
- Hours: Hours worked / Expected hours (160/month)

Range: 0-100
```

### Training Needs Detection

The system identifies training needs by analyzing:

1. **Performance Gaps**
   - Identifies assessment types with ratings < 3
   - Priority: High (rating < 2), Medium (2-3)

2. **Attendance Issues**
   - Threshold: 85% monthly attendance
   - Action: Professional conduct training

3. **Skill Assessment**
   - Analyzes historical assessment data
   - Recommends targeted training

### Recommended Actions

The system auto-generates actions based on:

| Score Range | Action | Urgency | Duration |
|------------|--------|---------|----------|
| 80-100 | Recognition & Incentive | Low | 30 days |
| 70-79 | Performance Monitoring | Medium | 14 days |
| 60-69 | Performance Improvement Plan | Medium | 21 days |
| <60 | Formal Performance Review | High | 7 days |
| Attendance <80% | Attendance Warning | High | 3 days |

---

## Integration with Main System

### Database Connection
- HR Manager uses the main `school_management.db`
- Shares connection with other modules
- All data persists across sessions

### Menu Integration
The HR Manager appears in the main navigation as:
- **Label**: 👔 HR Manager
- **Access Level**: Available to admin and authorized staff
- **Position**: Between Learning Support and Settings

### User Permissions
Currently, the HR Manager has:
- **Admin**: Full access to all features
- **Teachers**: Cannot access (feature planned for future)
- **Accountants**: Full read access (configurable)

---

## Troubleshooting

### Issue: "HR Manager is not available"
**Solution**: 
- Ensure `hr_manager.py` is in the main project directory
- Check for syntax errors: `python -m py_compile hr_manager.py`
- Restart the application

### Issue: Database table errors
**Solution**:
- Run: `python initialize_hr_database.py`
- Check database file exists: `database/school_management.db`
- Verify database permissions

### Issue: Payslip generates blank PDF
**Solution**:
- Ensure ReportLab is installed: `pip install reportlab`
- Check employee data is complete
- Verify timesheet data exists for selected month

### Issue: Performance score shows 0
**Solution**:
- Add assessment records for the employee
- Record attendance data
- Record timesheet hours
- Score updates automatically

---

## Development Notes

### Adding New Features

#### Add Custom Assessment Type
1. Add record to `employee_assessments` table
2. Adjust scoring algorithm if needed
3. Update training recommendation logic

#### Add New Deduction/Allowance Type
1. Insert data into `payroll_deductions` or `payroll_allowances`
2. Update payslip calculation if custom formula needed
3. Test PDF generation

#### Extend Training Programs
1. Add training program to `training_programs` table
2. Create enrollment record in `employee_training`
3. Update UI for new training categories

### Code Structure

#### Main Classes
- **HRAnalytics**: AI-powered analysis and recommendations
- **HRPayslipGenerator**: Payslip calculations and PDF generation
- **HRManagerUI**: User interface and display logic

#### Key Methods
- `calculate_employee_performance_score()`: Scoring algorithm
- `identify_training_needs()`: Detection logic
- `generate_recommended_actions()`: Action recommendations
- `calculate_payslip()`: Payroll calculations
- `generate_pdf_payslip()`: PDF creation

---

## Performance Optimization

### Database Indexes
Created for optimal query performance:
- `idx_employee_dept`: Employee department lookups
- `idx_timesheet_emp`: Timesheet queries
- `idx_attendance_emp`: Attendance lookups
- `idx_payslip_emp`: Payslip retrieval
- `idx_assessment_emp`: Assessment analysis
- `idx_training_emp`: Training status queries
- `idx_hr_actions_emp`: Action tracking

### Query Optimization
- Uses prepared statements for all SQL
- Indexes on frequently queried columns
- Efficient joins on foreign keys
- Limited date range queries (default 90 days)

---

## Future Enhancements

### Planned Features
- [ ] Employee self-service portal
- [ ] Performance graph visualization
- [ ] Advanced export options (Excel, CSV)
- [ ] Payslip email distribution
- [ ] Mobile app integration
- [ ] Multi-currency support
- [ ] Pension/Benefits calculation
- [ ] KPI tracking dashboard
- [ ] Compliance reporting
- [ ] Employee policies automation

### API Integration
- Performance sync with LMS
- External training provider integration
- Payroll system integration
- Email notification system

---

## Support & Contact

For issues or questions:
1. Check the Troubleshooting section
2. Review database initialization logs
3. Check application logs in console
4. Contact development team with error messages

---

## License

HR Manager Module
Part of Gaybeck Starkids School Management System
Copyright © 2024-2026. All rights reserved.

---

## Changelog

### Version 1.0.0 (March 5, 2026)
- Initial release
- Core features: Employee, Timesheet, Attendance, Payslips
- AI Analytics and Training Recommendations
- Database schema with 10 core tables
- Full PDF payslip generation
- Integration with main SMS system
