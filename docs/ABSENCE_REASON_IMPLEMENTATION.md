# Absence Reason Feature - Implementation Summary

## Overview
Added a comprehensive attendance reason tracking system to the School Management System that allows teachers to record why students are absent.

## Database Changes

### Schema Addition
Added `absence_reason` column to the `attendance` table:
```sql
absence_reason TEXT DEFAULT NULL
```

### Migration Support
Automatic migration for existing databases using:
```sql
ALTER TABLE attendance ADD COLUMN absence_reason TEXT DEFAULT NULL;
```

## UI Components

### Attendance Form Enhancement
Located in `sms.py` (lines 4857-4920), the attendance form now includes:

1. **Reason Dropdown (Combobox)**
   - Predefined reasons: "Illness", "Medical Appointment", "Family Emergency", "Permission", "Other"
   - Auto-populates when "Absent" is selected
   - Uses ttk.Combobox for clean UI

2. **Custom Details Field**
   - Text entry for additional information (e.g., "High fever and cough")
   - Optional field
   - Dynamically visible only when "Absent" is selected
   - Hidden for "Present" entries to keep UI clean

3. **Dynamic Visibility Logic**
   - Implemented with `StringVar.trace()` callback
   - Reason frame appears/hides based on attendance status
   - Improves UX by reducing visual clutter

## Business Logic

### Save Functionality
Updated `save_attendance()` method (lines 5176-5228):

```python
# Combine reason and details
if absence_reason and absence_details:
    reason_info = f"{absence_reason}: {absence_details}"
else:
    reason_info = absence_reason if absence_reason else None

# Save with proper reference
cursor.execute('''
    INSERT INTO attendance (student_id, date, status, absence_reason)
    VALUES (?, ?, ?, ?)
''', (student.get('db_id'), date, status, reason_info))
```

**Critical Fix:** Uses `student.get('db_id')` instead of `student['id']`
- `student['id']` = Registration ID (e.g., "STD001") - NOT suitable for foreign key
- `student.get('db_id')` = Database integer ID (e.g., 1) - Correct for foreign key reference

### Bulk Operations
Updated `save_bulk_attendance()` (lines 14430-14468) to handle absence_reason column for batch imports.

## Authorization & Access Control

### Teacher Access Restrictions
Added checks in:

1. **manage_student_attendance()** (lines 4851-4860)
   - Teachers can only access students from their assigned class
   - Verification against `teacher_classes` table
   - Raises exception if unauthorized

2. **write_student_remarks()** (lines 4962-4971)
   - Teachers can only write remarks for their assigned students
   - Prevents cross-class data modification

## Data Format

### Storage Format
Absence reasons are stored as combined text in single column:
```
"Illness"                          # Reason only
"Illness: High fever and cough"    # Reason: Custom details
```

This format allows:
- Easy querying for specific reasons
- Preservation of custom details
- Backward compatibility with existing reports

## Testing

### Test Suite
Location: `tests/test_attendance_reason.py`

Test Coverage:
- Column creation and migration
- INSERT operations with various reason combinations
- UPDATE operations on existing records
- NULL handling for present students
- Query functionality with custom details
- Database integrity validation

All tests passing ✅

## Integration Points

### Dependencies
- ttk.Combobox (built-in Tkinter)
- StringVar.trace() for reactive UI updates
- SQLite ALTER TABLE for migrations

### Backward Compatibility
- Column is nullable (DEFAULT NULL)
- Existing attendance records unaffected
- No breaking changes to API

## Usage Example

### For Teachers
1. Mark student as "Absent"
2. Select reason from dropdown (or type custom)
3. (Optional) Add details about absence
4. Save attendance record
5. Absence with reason is stored in database

### For Reports
```python
# Query absences with reasons
cursor.execute('''
    SELECT student_name, date, absence_reason 
    FROM attendance 
    WHERE status = 'Absent' AND absence_reason IS NOT NULL
    ORDER BY date DESC
''')
```

## Files Modified
- `sms.py` - Core application (UI, business logic, database)
- `ui_components.py` - Fixed import error for optional enhanced_ews module
- `tests/test_attendance_reason.py` - New comprehensive test suite

## Performance Considerations
- Column indexed implicitly through primary key + date
- TEXT storage minimal (typical reasons < 100 chars)
- No performance impact on existing queries
- Optional field keeps NULL overhead minimal
