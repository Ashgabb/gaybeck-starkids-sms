# Migration Guide: Desktop to Web

## Overview
This guide helps you migrate data from the original Tkinter desktop application to the Django web application.

## Pre-Migration Checklist
- [ ] Backup original SQLite database
- [ ] Test web application setup
- [ ] Plan migration during low-usage time
- [ ] Have administrator credentials ready
- [ ] Document current system state

## Step 1: Backup Your Data

### From Desktop App
```bash
# Copy the database file
copy "path\to\school_management.db" "path\to\backup_school_management.db"
```

### From Web App (Before Migration)
```bash
python manage.py dumpdata > backup_before_migration.json
```

## Step 2: Export Data from Desktop App

Create a Python script to export data:

```python
import sqlite3
import json
from pathlib import Path

# Connect to original database
conn = sqlite3.connect('database/school_management.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

data = {}
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data[table_name] = [dict(zip(columns, row)) for row in rows]

# Save to JSON
with open('exported_data.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

conn.close()
print("Data exported successfully!")
```

## Step 3: Transform Data

The database schemas differ between desktop and web versions. Create a transformation script:

```python
import json
from datetime import datetime

# Load exported data
with open('exported_data.json', 'r') as f:
    data = json.load(f)

# Transform users
admin_user = {
    "email": "admin@school.com",
    "password": "set_strong_password",
    "first_name": "Administrator",
    "last_name": "User",
    "role": "admin",
    "is_active": True
}

# Transform students
students = []
if 'students' in data:
    for student in data['students']:
        students.append({
            "name": f"{student.get('first_name', '')} {student.get('last_name', '')}",
            "registration_number": student.get('student_id', ''),
            "date_of_birth": student.get('dob', '2000-01-01'),
            "gender": student.get('gender', 'M'),
            "email": student.get('email', ''),
            "phone": student.get('phone', ''),
            "address": student.get('address', ''),
            "class_name": student.get('class_name', ''),
            "guardian_name": student.get('guardian_name', ''),
            "guardian_phone": student.get('guardian_phone', ''),
            "is_active": student.get('is_active', True)
        })

print(f"Transformed {len(students)} students")
```

## Step 4: Import Data into Web App

### Option A: Django Management Command

Create `web_app/accounts/management/commands/import_data.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Import data from desktop application'
    
    def handle(self, *args, **options):
        with open('exported_data.json', 'r') as f:
            data = json.load(f)
        
        # Import students
        for student_data in data.get('students', []):
            Student.objects.create(
                name=student_data['name'],
                registration_number=student_data['registration_number'],
                date_of_birth=student_data['date_of_birth'],
                gender=student_data['gender'],
                email=student_data.get('email', ''),
                phone=student_data.get('phone', ''),
                address=student_data['address'],
                class_name=student_data['class_name'],
                guardian_name=student_data['guardian_name'],
                guardian_phone=student_data['guardian_phone'],
                is_active=student_data.get('is_active', True)
            )
        
        self.stdout.write(
            self.style.SUCCESS('Data imported successfully!')
        )
```

Run with:
```bash
python manage.py import_data
```

### Option B: Django Admin

1. Create CSV files from exported data
2. Use Django admin's import functionality
3. Or manually enter data through the web interface

### Option C: Manual Import

1. Login as administrator
2. Use "Add Student", "Add Teacher" etc. buttons
3. Populate records manually

## Step 5: Verify Data

### Check Student Count
```python
python manage.py shell
from students.models import Student
print(f"Total students: {Student.objects.count()}")
```

### Generate Reports
```bash
python manage.py shell < scripts/verify_migration.py
```

## Step 6: Test All Features

### Test Attendance
- [ ] Record attendance for a class
- [ ] View attendance records
- [ ] Edit attendance

### Test Fees
- [ ] Create fee entries
- [ ] Record payments
- [ ] View payment history

### Test Grading
- [ ] Add grades for students
- [ ] View grade reports
- [ ] Check grade calculations

### Test Analytics
- [ ] View dashboard
- [ ] Check student analytics
- [ ] View class analytics

## Step 7: Troubleshooting

### Data Not Appearing
```bash
python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput
```

### User Login Issues
```bash
python manage.py changepassword admin
```

### Missing Records
Check the import log:
```python
python manage.py shell
from accounts.models import ActivityLog
ActivityLog.objects.all().count()
```

## Step 8: Cutover

### Timeline
1. **Test Phase**: 1-2 weeks in parallel
2. **Partial Migration**: Migrate one class at a time
3. **Full Migration**: Complete data transfer
4. **Verification**: 1 week parallel testing
5. **Go Live**: Switch to web app only

### Rollback Plan
If issues occur:
1. Restore backup: `python manage.py loaddata backup_before_migration.json`
2. Switch back to desktop app
3. Investigate issues
4. Retry migration

## Best Practices

1. **Schedule Migration During Off-Peak**
   - Avoid term starts/ends
   - Plan during school holidays if possible

2. **Train Users First**
   - Conduct web app training sessions
   - Prepare documentation
   - Have support team ready

3. **Test Thoroughly**
   - Test all features
   - Test with real data volume
   - Test with different user roles

4. **Document Changes**
   - Keep migration log
   - Document any data transformations
   - Note any manual adjustments

5. **Maintain Backups**
   - Keep old database for 30 days
   - Take daily web app backups
   - Test backup restoration process

## Post-Migration

### Week 1
- [ ] Monitor system performance
- [ ] Check for data inconsistencies
- [ ] Gather user feedback
- [ ] Fix critical issues

### Week 2-4
- [ ] Optimize database
- [ ] Train more users
- [ ] Address feature requests
- [ ] Plan enhancements

### Month 2+
- [ ] Archive old data
- [ ] Plan additional features
- [ ] Scale infrastructure if needed
- [ ] Regular backups and maintenance

## Common Issues & Solutions

### Issue: Missing attendance records
**Solution**: Check date formats match expected format

### Issue: Fee calculations incorrect
**Solution**: Verify StudentFee model calculations, recalculate using management command

### Issue: Students not appearing in classes
**Solution**: Check class_name field consistency, run data cleaning script

### Issue: Performance issues
**Solution**: Create database indexes, optimize queries, consider PostgreSQL

## Additional Resources

- Django Data Migration Guide
- Database Backup & Recovery
- Data Validation Scripts
- User Training Materials

---

For help with migration, contact your system administrator.
