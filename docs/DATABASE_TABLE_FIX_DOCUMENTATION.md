# DATABASE TABLE REFERENCE FIX

## Issue Fixed: "Error updating fee statistics: no such table: fee_payments"

### Problem Description:
The application was trying to query a `fee_payments` table that doesn't exist in the database schema. The actual table for fee data is `fees`.

### Root Cause:
- Incorrect table name references in fee statistics calculations
- The queries were using `fee_payments` instead of `fees`

### Files Modified:
- **sms.py** (Lines 9528 and 9545 approximately)

### Changes Made:

#### 1. Fixed total collected fees query:
**Before:**
```sql
SELECT SUM(amount_paid) FROM fee_payments WHERE amount_paid > 0
```

**After:**
```sql
SELECT SUM(amount_paid) FROM fees WHERE amount_paid > 0
```

#### 2. Fixed monthly collections query:
**Before:**
```sql
SELECT SUM(amount_paid) FROM fee_payments 
WHERE strftime('%Y-%m', payment_date) = ?
```

**After:**
```sql
SELECT SUM(amount_paid) FROM fees 
WHERE strftime('%Y-%m', payment_date) = ?
```

### Verification:
- ✅ Application now runs without database errors
- ✅ Fee statistics calculations use correct table references
- ✅ All fee-related queries now work with existing database schema

### Database Schema Reference:
The correct table structure for fees is:
```sql
CREATE TABLE IF NOT EXISTS fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    month TEXT,
    year INTEGER,
    amount_due REAL,
    amount_paid REAL,
    arrears REAL,
    feeding_fee_paid BOOLEAN DEFAULT 0,
    bus_fee_paid BOOLEAN DEFAULT 0,
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES students (id)
)
```

### Impact:
This fix ensures that:
1. Fee statistics display correctly in the dashboard
2. Real-time fee calculations work properly
3. The comprehensive synchronization system functions without errors
4. All fee-related reporting operates on the correct data source

The application is now fully functional with proper fee-financial synchronization as implemented in the comprehensive sync system.