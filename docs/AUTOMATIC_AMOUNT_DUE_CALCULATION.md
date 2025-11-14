# Automatic Amount Due Calculation - Fee Management

## Overview
Enhanced the fee management system to automatically calculate and populate the "Amount Due" field when a student is selected.

## Calculation Formula
```
Amount Due = Total Arrears + Current Month's Fee
```

Where:
- **Total Arrears**: Sum of all previous unpaid balances (arrears) from the student's fee history
- **Current Month's Fee**: The monthly_fee value from the student's record

## Implementation

### UI Changes
- Added event binding to the student selection combobox
- When a student is selected, the "Amount Due" field auto-populates

### Backend Function
**`calculate_amount_due(event=None)`**
1. Gets selected student ID
2. Queries student's monthly_fee from students table
3. Sums all arrears from fees table for that student
4. Calculates: amount_due = arrears + monthly_fee
5. Populates the "Amount Due" field with calculated value

### Code Location
- **File**: `sms.py`
- **Function**: `calculate_amount_due()` (around line 11486)
- **Trigger**: `fee_student_cb.bind('<<ComboboxSelected>>', self.calculate_amount_due)`

## Usage

**Recording a New Fee Payment:**
1. Select student from dropdown
   - ✨ Amount Due automatically calculated and displayed
2. The field shows: Previous arrears + Monthly fee
3. Enter amount paid
4. Click "Add Payment"
   - System calculates new arrears: (amount_due - amount_paid)

## Example Calculation

**Student: David Nkrumah**
- Monthly Fee: GHS 200.00
- Previous Arrears: GHS 0.00
- **Auto-calculated Amount Due: GHS 200.00**

If student had arrears:
- Monthly Fee: GHS 200.00
- Previous Arrears: GHS 150.00
- **Auto-calculated Amount Due: GHS 350.00**

## Benefits
- ✅ Eliminates manual calculation errors
- ✅ Ensures consistent fee tracking
- ✅ Automatically accounts for outstanding balances
- ✅ Speeds up fee payment entry
- ✅ Reduces data entry errors

## Testing
Tested with sample student data:
- Student with no arrears: Correctly shows monthly fee only
- Student with arrears: Correctly sums arrears + monthly fee
- All calculations verified against database records

## Files Modified
1. **sms.py**
   - Added `calculate_amount_due()` function
   - Bound student combobox selection event
   - Auto-populates amount_due field

2. **tests/test_amount_due_calculation.py**
   - Verification script showing calculation logic
   - Sample output with real student data
