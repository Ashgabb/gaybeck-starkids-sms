"""
Sync Fees with Financial Management System

This script synchronizes all existing fee payments with the financial management system
by creating corresponding financial transaction records for each fee payment.
"""

import sqlite3
from datetime import datetime

def sync_fees_to_financial():
    """Sync all existing fee payments to financial transactions"""
    
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    
    try:
        print("=" * 70)
        print("FEES TO FINANCIAL MANAGEMENT SYNC")
        print("=" * 70)
        
        # First, ensure the 'School Fees' category exists
        cursor.execute("SELECT id FROM financial_categories WHERE category_name = 'School Fees'")
        category_result = cursor.fetchone()
        
        if not category_result:
            print("\nCreating 'School Fees' financial category...")
            cursor.execute("""
                INSERT INTO financial_categories (category_name, category_type, description)
                VALUES ('School Fees', 'income', 'Student tuition and school fees')
            """)
            conn.commit()
            category_id = cursor.lastrowid
            print(f"  Created category with ID: {category_id}")
        else:
            category_id = category_result[0]
            print(f"\n'School Fees' category exists (ID: {category_id})")
        
        # Get all fee payments that don't have corresponding financial transactions
        cursor.execute('''
            SELECT f.id, f.student_id, f.amount_paid, f.payment_date, f.month, f.year, s.name
            FROM fees f
            JOIN students s ON f.student_id = s.id
            WHERE f.amount_paid > 0 
            AND NOT EXISTS (
                SELECT 1 FROM financial_transactions ft 
                WHERE ft.reference_number = 'FEE-' || f.id
            )
            ORDER BY f.payment_date, f.id
        ''')
        
        unsynced_fees = cursor.fetchall()
        
        if not unsynced_fees:
            print("\nAll fees are already synced with financial transactions!")
            return
        
        print(f"\nFound {len(unsynced_fees)} fee payments to sync")
        print("-" * 70)
        
        # Calculate totals
        total_amount = sum(fee[2] for fee in unsynced_fees)
        print(f"Total amount to be synced: GHS {total_amount:,.2f}\n")
        
        # Confirm before proceeding
        response = input("Do you want to proceed with syncing? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Sync cancelled.")
            return
        
        print("\nSyncing fee payments to financial transactions...\n")
        
        synced_count = 0
        synced_amount = 0.0
        
        for fee_id, student_id, amount_paid, payment_date, month, year, student_name in unsynced_fees:
            try:
                # Create description
                description = f"School Fee Payment - {student_name} (Fee ID: {fee_id})"
                period_info = f"{month} {year}"
                
                # Insert financial transaction
                cursor.execute('''
                    INSERT INTO financial_transactions (
                        transaction_date, category_id, transaction_type, amount, description,
                        reference_number, payment_method, created_by, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    payment_date or datetime.now().strftime('%Y-%m-%d'),
                    category_id,
                    'income',
                    amount_paid,
                    description,
                    f"FEE-{fee_id}",
                    'Cash',
                    1,  # Default admin user
                    f"Synced from fees table - {period_info}"
                ))
                
                synced_count += 1
                synced_amount += amount_paid
                
                print(f"  [{synced_count}/{len(unsynced_fees)}] Synced Fee #{fee_id}: {student_name} - GHS {amount_paid:,.2f} ({period_info})")
                
            except Exception as e:
                print(f"  ERROR syncing Fee #{fee_id}: {e}")
                continue
        
        # Commit all transactions
        conn.commit()
        
        print("\n" + "=" * 70)
        print("SYNC COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(f"Total fees synced: {synced_count}")
        print(f"Total amount synced: GHS {synced_amount:,.2f}")
        print("\nThe Fees Manager and Financial Manager are now synchronized!")
        
    except Exception as e:
        print(f"\nERROR during sync: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    sync_fees_to_financial()
