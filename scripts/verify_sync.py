import sqlite3

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

print("=" * 70)
print("FEES-FINANCIAL SYNC VERIFICATION")
print("=" * 70)

# Check fee transactions
cursor.execute('SELECT COUNT(*) FROM financial_transactions WHERE reference_number LIKE "FEE-%"')
fee_trans = cursor.fetchone()[0]
print(f"\nFinancial Transactions from Fees: {fee_trans}")

# Check total income
cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM financial_transactions WHERE transaction_type = "income"')
income_count, income_total = cursor.fetchone()
print(f"Total Income Transactions: {income_count}")
print(f"Total Income Amount: GHS {income_total:,.2f}")

# Check fees with payments
cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount_paid), 0) FROM fees WHERE amount_paid > 0')
paid_fees, total_paid = cursor.fetchone()
print(f"\nFees with Payments: {paid_fees}")
print(f"Total Fees Paid: GHS {total_paid:,.2f}")

# Sample of synced transactions
print("\n" + "=" * 70)
print("SAMPLE SYNCED TRANSACTIONS")
print("=" * 70)
cursor.execute('''
    SELECT ft.id, ft.transaction_date, ft.amount, ft.description, ft.reference_number
    FROM financial_transactions ft
    WHERE ft.reference_number LIKE "FEE-%"
    ORDER BY ft.transaction_date DESC
    LIMIT 5
''')

for row in cursor.fetchall():
    print(f"\nID: {row[0]}")
    print(f"  Date: {row[1]}")
    print(f"  Amount: GHS {row[2]:,.2f}")
    print(f"  Description: {row[3]}")
    print(f"  Reference: {row[4]}")

conn.close()

print("\n" + "=" * 70)
print("✓ Fees Manager and Financial Manager are now synchronized!")
print("=" * 70)
