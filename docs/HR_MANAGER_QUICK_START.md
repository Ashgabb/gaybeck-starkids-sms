# HR Manager - Quick Start Guide

## 📋 Overview

The **HR Manager** module provides comprehensive employee management with AI-powered analytics. Track timesheets, attendance, generate payslips, and receive intelligent training recommendations.

---

## 🚀 Getting Started

### 1. Initialize HR Database (First Time Only)

```bash
python initialize_hr_database.py
```

Expected output:
```
✓ Employees table created
✓ Timesheets table created
✓ Employee Attendance table created
... [more tables]
✅ HR Database Initialization Complete!
```

### 2. Launch the Application

```bash
python sms.py
```

### 3. Access HR Manager

- Login as Admin
- In the navigation sidebar, click "👔 HR Manager"
- HR Manager window opens with tabbed interface

---

## 📊 Feature Quick Reference

| Feature | Tab | What It Does |
|---------|-----|-------------|
| **Add Employees** | Employees | Register new staff members |
| **Track Hours** | Timesheets | Record daily working hours and overtime |
| **Mark Attendance** | Attendance | Track present/absent/leave status |
| **Generate Payslips** | Payslips | Create monthly salary documents |
| **Analyze Performance** | Performance & Training | View AI-scored employee metrics |
| **AI Insights** | AI Insights | View company-wide HR analytics |

---

## 👤 Employee Management

### Add an Employee

```
1. Click "➕ Add Employee"
2. Fill in:
   - Name (required)
   - Position (e.g., "Teacher", "Accountant")
   - Department (e.g., "Academic", "Admin")
   - Salary (annual amount)
   - Email (optional)
   - Phone (optional)
3. Click "Save"
```

**Example:**
- Name: John Doe
- Position: Senior Teacher
- Department: Academic
- Salary: 35000

### View Employee Details

1. Select employee from the list
2. Right panel shows:
   - Personal information
   - Performance Score
   - Status

---

## ⏰ Timesheet Management

### Record Hours

```
1. Select employee and month/year
2. Click "Load Timesheet"
3. Enter for each day:
   - Hours Worked (typically 8)
   - Overtime Hours (additional hours)
   - Leave Hours (if applicable)
4. Save
```

**Standard Monthly Hours:** 160 (20 working days × 8 hours)

**Overtime Calculation:** Extra hours × hourly rate × 1.5

---

## ✅ Attendance Tracking

### Mark Daily Attendance

```
1. Select employee
2. Select date
3. Choose status:
   ✓ Present  - Employee worked full day
   ✗ Absent   - Employee did not come
   ✋ Leave    - Employee on approved leave
   ⏰ Late     - Employee came late
4. Add notes (optional)
5. Save
```

**Impact on Performance Score:**
- Attendance below 75%: Triggers training recommendation
- Attendance below 80%: Issues warning

---

## 💰 Payslip Generation

### Generate Monthly Payslip

```
1. Go to "Payslips" tab
2. Select employee
3. Select month and year
4. Click "Preview Payslip"
```

**Payslip Shows:**
```
EARNINGS:
- Basic Pay: (Salary / 160) × Hours Worked
- Overtime: Overtime Hours × Hourly Rate × 1.5
- Allowances: Any additional payments
- Gross Pay: Sum of all earnings

DEDUCTIONS:
- Taxes, insurance, or other deductions
- Total Deductions

NET PAY: Gross Pay - Deductions
```

### Export as PDF

```
1. Preview payslip (above steps)
2. Click "Generate PDF"
3. Choose save location
4. PDF download complete with professional layout
```

---

## 🎯 Performance & Training

### View Performance Analysis

```
1. Go to "Performance & Training" tab
2. Select an employee
3. System shows:
   - Performance Score (0-100)
   - Training Needs
   - Recommended Actions
```

### Performance Score Breakdown

| Score | Level | Actions |
|-------|-------|---------|
| 80-100 | Excellent | Recognition, incentives |
| 60-79 | Satisfactory | Regular monitoring, skill development |
| 0-59 | Below Expectations | Improvement plan, intensive training |

### Training Recommendations

System automatically identifies needs like:
- **Performance Gaps:** Low scores in specific skills
- **Attendance Issues:** Attendance below 85%
- **Development Areas:** Skills needing improvement

---

## 🤖 AI Insights

### View Overall HR Analytics

```
1. Go to "AI Insights" tab
2. Click "🎯 Overall Performance Analysis"
```

**Shows:**
- High Performers %
- Medium Performers %
- Low Performers %
- Recommendations for each group

### Department Analytics

```
1. Go to "AI Insights" tab
2. Click "📊 Department Analytics"
```

**Shows:**
- Performance by department
- Training needs by area
- Staffing efficiency

---

## 📈 AI Features Explained

### Performance Scoring (0-100)

```
Score = (Attendance × 0.3) + (Assessment × 0.4) + (Hours × 0.3)

Example:
- Attendance: 90% × 0.3 = 27 points
- Assessment Rating: 4/5 × 20 × 0.4 = 32 points
- Hours: 160/160 × 100 × 0.3 = 30 points
- Total Score: 89/100
```

### Automatic Training Recommendations

The system analyzes:
1. **Performance assessments** → Identifies weak areas
2. **Attendance patterns** → Detects issues
3. **Work hours** → Checks compliance
4. **Historical data** → Trends analysis

**Result:** Smart, personalized training suggestions

### Suggested HR Actions

The system recommends actions like:

| When | Action | Details |
|------|--------|---------|
| Score ≥ 80 | Recognition | Bonus/increment eligibility |
| Score 60-79 | Monitor | Check-in conversations |
| Score < 60 | Improvement Plan | 7-day action plan |
| Attendance < 80% | Warning | Formal notice |

---

## 💾 Data Export & Reporting

### Export Employee List

```
1. On Employees tab
2. Right-click employee list
3. Select "Export to CSV"
4. Choose save location
```

### Generate Reports

**Monthly Payroll Report:**
- Lists all payslips for month
- Shows deductions and allowances
- Includes net payroll total

**Attendance Report:**
- Employee attendance summary
- Department-wise attendance
- Month-on-month comparison

**Performance Report:**
- Employee performance scores
- Training recommendations
- Action item status

---

## ⚠️ Common Tasks

### Calculate Monthly Payroll for All Employees

```
1. Go to Payslips tab
2. For each employee:
   - Ensure timesheet is completed
   - Preview payslip
   - Generate PDF
3. All payslips ready for payment
```

### Identify At-Risk Employees

```
1. Go to AI Insights
2. Look at "Low Performers" section
3. Review their training needs
4. Create improvement plans
```

### Track Absence Patterns

```
1. Go to Attendance tab
2. Select employee and date range
3. Review status history
4. Identify patterns
5. Take action if needed
```

---

## 🔍 Troubleshooting

### Q: "HR Manager is not available"
**A:** Restart the application. Ensure `hr_manager.py` is in the project root.

### Q: Performance score shows 0
**A:** 
- Make sure timesheet hours are recorded
- Add attendance records
- Create performance assessments

### Q: Payslip shows incomplete data
**A:** 
- Verify employee salary is set
- Check timesheet has hours for the month
- Ensure ReportLab is installed (`pip install reportlab`)

### Q: Can't find employee in dropdown
**A:** 
- Make sure employee was saved successfully
- Click Refresh to reload list
- Check employee status is "Active"

---

## 📚 Database Location

The HR data is stored in:
```
school_management.db
```

Located in the project root directory.

---

## 🛠️ Advanced Setup

### For Developers

To customize the HR Manager:

1. Edit `hr_manager.py` for UI changes
2. Update scoring algorithm in `HRAnalytics` class
3. Modify database schema in `initialize_hr_database.py`
4. Add new training types in database

### Integration with LMS

The HR Manager data can be linked to:
- Student progress tracking
- Teacher effectiveness metrics
- Course performance analysis
- Learning outcome assessment

---

## 📞 Support

**For Issues:**
1. Check the troubleshooting section above
2. Verify database is initialized: `python initialize_hr_database.py`
3. Check if Python syntax is correct: `python -m py_compile hr_manager.py`

**For Feature Requests:**
- Contact development team with specific use case
- Provide example of desired functionality

---

## 🎓 Key Metrics Tracked

### Employee Metrics
- ✓ Attendance rate
- ✓ Performance rating
- ✓ Hours worked vs. expected
- ✓ Training completion
- ✓ Salary & deductions

### Department Metrics
- ✓ Average performance score
- ✓ Overall attendance rate
- ✓ Training coverage %
- ✓ Payroll accuracy

### Organization Metrics
- ✓ % High performers
- ✓ % At-risk employees
- ✓ Training ROI
- ✓ Staff retention trends

---

## ✨ Best Practices

1. **Regular Updates**
   - Update timesheets weekly
   - Mark attendance daily
   - Review performance monthly

2. **Training**
   - Act on recommendations quickly
   - Track training completion
   - Document skills gained

3. **Communication**
   - Share performance scores annually
   - Discuss training needs quarterly
   - Address warnings immediately

4. **Documentation**
   - Keep employee records current
   - Document all assessments
   - Archive payslips annually

---

**Version:** 1.0.0  
**Last Updated:** March 5, 2026  
**Status:** ✅ Production Ready
