# Fee Payment System Enhancement

## Overview
Updated the fee payment system to include specific fee types and payment modes for better tracking and categorization.

## Database Changes

### Added Columns to `fees` Table:
1. **fee_type** (TEXT, DEFAULT 'Tuition')
   - Values: Tuition, Feeding, Bus
   
2. **payment_mode** (TEXT, DEFAULT 'Cash')
   - Values: Cash, MoMo, Bank

## UI Changes

### Fee Management Form
Added two new dropdown fields:

1. **Fee Type Dropdown**
   - Options: Tuition, Feeding, Bus
   - Default: Tuition
   - Location: Below amount fields

2. **Payment Mode Dropdown**
   - Options: Cash, MoMo, Bank
   - Default: Cash
   - Location: Next to Fee Type

### Fee Records Table
Updated columns to display:
- ID
- Student
- Month
- Year
- **Fee Type** (new)
- Amount Due
- Amount Paid
- Arrears
- **Payment Mode** (new)
- Feeding (legacy field)
- Bus (legacy field)
- Payment Date

## Functionality Updates

### Add Fee Payment
- Now captures fee type and payment mode
- Stores values in database with each transaction
- Creates corresponding financial transaction

### Update Fee Payment
- Allows updating fee type and payment mode
- Updates database and synchronizes with financial records

### Load Fees
- Displays fee type and payment mode in the table
- Shows "Tuition" as default for existing records without fee_type
- Shows "Cash" as default for existing records without payment_mode

### Select Fee Record
- Populates fee type dropdown when selecting a record
- Populates payment mode dropdown when selecting a record
- Maintains backward compatibility with legacy feeding/bus checkboxes

## Migration Notes

All existing fee records will have:
- fee_type = "Tuition" (default)
- payment_mode = "Cash" (default)

The legacy feeding_fee_paid and bus_fee_paid boolean fields are maintained for backward compatibility and historical data.

## Files Modified

1. **sms.py**
   - Updated setup_fee_management() to add fee type and payment mode dropdowns
   - Updated add_fee() to save fee type and payment mode
   - Updated update_fee() to update fee type and payment mode
   - Updated load_fees() to display fee type and payment mode
   - Updated on_fee_select() to populate fee type and payment mode fields
   - Updated tree view columns to include new fields

2. **Database Schema**
   - Migration script: tests/update_fees_schema.py
   - Added fee_type column (TEXT)
   - Added payment_mode column (TEXT)

## Testing

✅ Schema migration completed successfully
✅ Application launches without errors
✅ New dropdowns added to fee management form
✅ Table columns updated to display new fields
✅ Add/Update/Select operations updated

## Usage

**Recording a New Fee Payment:**
1. Select student
2. Choose month and year
3. Select fee type (Tuition/Feeding/Bus)
4. Enter amount due and amount paid
5. Select payment mode (Cash/MoMo/Bank)
6. Optionally check feeding/bus fee flags
7. Set payment date
8. Click "Add Payment"

**Benefits:**
- Better categorization of fee types
- Track payment methods for reconciliation
- Improved reporting capabilities
- Clear distinction between tuition, feeding, and bus fees
- Support for mobile money and bank transfers
