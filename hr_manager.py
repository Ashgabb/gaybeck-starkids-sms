"""
HR Manager Module for School Management System
Handles employee management, timesheets, payslips, and AI-powered training recommendations
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import sqlite3
from datetime import datetime, date, timedelta
import calendar
import os
import csv
from decimal import Decimal
try:
    from tkcalendar import DateEntry
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class HRAnalytics:
    """AI-powered HR analytics for performance and training recommendations"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
    
    def calculate_employee_performance_score(self, employee_id):
        """Calculate overall performance score for an employee (0-100)"""
        try:
            # Get attendance data
            self.cursor.execute("""
                SELECT COUNT(*) as total_days, 
                       SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) as present_days
                FROM employee_attendance
                WHERE employee_id = ? AND date >= date('now', '-90 days')
            """, (employee_id,))
            attendance_data = self.cursor.fetchone()
            
            total_days = attendance_data[0] or 1
            present_days = attendance_data[1] or 0
            attendance_score = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Get performance ratings
            self.cursor.execute("""
                SELECT AVG(performance_rating) as avg_rating
                FROM employee_assessments
                WHERE employee_id = ?
            """, (employee_id,))
            assessment_data = self.cursor.fetchone()
            performance_score = (assessment_data[0] or 0) * 20  # Scale to 0-100
            
            # Get hours worked vs expected
            self.cursor.execute("""
                SELECT SUM(hours_worked) as total_hours
                FROM timesheets
                WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, date.today().month, date.today().year))
            timesheet_data = self.cursor.fetchone()
            hours_worked = timesheet_data[0] or 0
            expected_hours = 160  # Standard monthly hours
            hours_score = min((hours_worked / expected_hours * 100), 100)
            
            # Calculate weighted score
            overall_score = (attendance_score * 0.3) + (performance_score * 0.4) + (hours_score * 0.3)
            return min(round(overall_score, 2), 100)
        
        except Exception as e:
            print(f"Error calculating performance score: {e}")
            return 0
    
    def identify_training_needs(self, employee_id):
        """Identify training needs based on performance gaps"""
        try:
            training_needs = []
            score = self.calculate_employee_performance_score(employee_id)
            
            # Get employee details
            self.cursor.execute("""
                SELECT name, position, department
                FROM employees WHERE id = ?
            """, (employee_id,))
            employee = self.cursor.fetchone()
            
            if not employee:
                return []
            
            # Analyze specific gaps
            self.cursor.execute("""
                SELECT performance_rating, assessment_type
                FROM employee_assessments
                WHERE employee_id = ?
                ORDER BY date DESC
                LIMIT 5
            """, (employee_id,))
            
            assessments = self.cursor.fetchall()
            for rating, assessment_type in assessments:
                if rating and rating < 3:  # Rating out of 5
                    training_needs.append({
                        'area': assessment_type,
                        'priority': 'High' if rating < 2 else 'Medium',
                        'reason': f'Performance gap in {assessment_type}'
                    })
            
            # Check attendance
            self.cursor.execute("""
                SELECT COUNT(*) as total_days, 
                       SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) as present_days
                FROM employee_attendance
                WHERE employee_id = ? AND date >= date('now', '-30 days')
            """, (employee_id,))
            att_data = self.cursor.fetchone()
            
            if att_data[0] > 0:
                att_rate = (att_data[1] / att_data[0] * 100) if att_data[0] > 0 else 0
                if att_rate < 85:
                    training_needs.append({
                        'area': 'Professional Conduct',
                        'priority': 'High',
                        'reason': f'Attendance rate ({att_rate:.0f}%) below standard (85%)'
                    })
            
            return training_needs
        
        except Exception as e:
            print(f"Error identifying training needs: {e}")
            return []
    
    def generate_recommended_actions(self, employee_id):
        """Generate recommended HR actions based on performance data"""
        try:
            actions = []
            score = self.calculate_employee_performance_score(employee_id)
            
            if score >= 80:
                actions.append({
                    'action': 'Recognition & Incentive',
                    'description': 'Consider salary increment or bonus',
                    'urgency': 'Low',
                    'dueDate': (date.today() + timedelta(days=30)).isoformat()
                })
            elif score < 60:
                actions.append({
                    'action': 'Performance Improvement Plan',
                    'description': 'Schedule meeting to discuss performance gaps',
                    'urgency': 'High',
                    'dueDate': (date.today() + timedelta(days=7)).isoformat()
                })
            elif score < 70:
                actions.append({
                    'action': 'Performance Monitoring',
                    'description': 'Schedule check-in to monitor improvement',
                    'urgency': 'Medium',
                    'dueDate': (date.today() + timedelta(days=14)).isoformat()
                })
            
            # Check for attendance issues
            self.cursor.execute("""
                SELECT COUNT(*) as total_days, 
                       SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) as present_days
                FROM employee_attendance
                WHERE employee_id = ? AND date >= date('now', '-60 days')
            """, (employee_id,))
            att_data = self.cursor.fetchone()
            
            if att_data[0] > 0:
                att_rate = (att_data[1] / att_data[0] * 100) if att_data[0] > 0 else 0
                if att_rate < 80:
                    actions.append({
                        'action': 'Attendance Warning',
                        'description': 'Issue attendance notice and warning',
                        'urgency': 'High',
                        'dueDate': (date.today() + timedelta(days=3)).isoformat()
                    })
            
            return actions
        
        except Exception as e:
            print(f"Error generating recommended actions: {e}")
            return []


class HRPayslipGenerator:
    """Generate payslips for employees"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
    
    def calculate_payslip(self, employee_id, month, year):
        """Calculate payslip data for an employee"""
        try:
            # Get employee info
            self.cursor.execute("""
                SELECT id, name, position, salary, email, department
                FROM employees WHERE id = ?
            """, (employee_id,))
            employee = self.cursor.fetchone()
            
            if not employee:
                return None
            
            emp_id, name, position, salary, email, department = employee
            
            # Get timesheet data
            self.cursor.execute("""
                SELECT SUM(hours_worked), AVG(overtime_hours), SUM(leave_hours)
                FROM timesheets
                WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, month, year))
            timesheet = self.cursor.fetchone()
            
            hours_worked = timesheet[0] or 0
            overtime_hours = timesheet[1] or 0
            leave_hours = timesheet[2] or 0
            
            # Get deductions
            self.cursor.execute("""
                SELECT SUM(amount) as total_deductions
                FROM payroll_deductions
                WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, month, year))
            deductions = self.cursor.fetchone()[0] or 0
            
            # Get allowances
            self.cursor.execute("""
                SELECT SUM(amount) as total_allowances
                FROM payroll_allowances
                WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, month, year))
            allowances = self.cursor.fetchone()[0] or 0
            
            # Calculate basic pay
            expected_hours = 160  # Standard monthly hours
            basic_pay = salary if hours_worked >= expected_hours else (salary / expected_hours) * hours_worked
            
            # Overtime pay (1.5x hourly rate)
            hourly_rate = salary / expected_hours
            overtime_pay = overtime_hours * hourly_rate * 1.5
            
            # Gross pay
            gross_pay = basic_pay + overtime_pay + allowances
            
            # Net pay
            net_pay = gross_pay - deductions
            
            return {
                'employee_id': emp_id,
                'employee_name': name,
                'position': position,
                'department': department,
                'email': email,
                'month': month,
                'year': year,
                'basic_pay': round(basic_pay, 2),
                'overtime_pay': round(overtime_pay, 2),
                'allowances': round(allowances, 2),
                'gross_pay': round(gross_pay, 2),
                'deductions': round(deductions, 2),
                'net_pay': round(net_pay, 2),
                'hours_worked': hours_worked,
                'overtime_hours': overtime_hours,
                'leave_hours': leave_hours
            }
        
        except Exception as e:
            print(f"Error calculating payslip: {e}")
            return None
    
    def generate_pdf_payslip(self, payslip_data, output_path, currency_symbol='$'):
        """Generate PDF payslip"""
        if not PDF_AVAILABLE:
            messagebox.showerror("Error", "PDF generation not available")
            return False
        
        try:
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=20,
                alignment=1  # Center
            )
            elements.append(Paragraph("EMPLOYEE PAYSLIP", title_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Employee info
            emp_info = [
                ['Employee Name:', payslip_data['employee_name']],
                ['Position:', payslip_data['position']],
                ['Department:', payslip_data['department']],
                ['Period:', f"{payslip_data['month']}/{payslip_data['year']}"]
            ]
            
            emp_table = Table(emp_info, colWidths=[2*inch, 4*inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(emp_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Earnings
            earnings_data = [
                ['EARNINGS', 'Amount'],
                ['Basic Pay', f"{currency_symbol}{payslip_data['basic_pay']:.2f}"],
                ['Overtime Pay', f"{currency_symbol}{payslip_data['overtime_pay']:.2f}"],
                ['Allowances', f"{currency_symbol}{payslip_data['allowances']:.2f}"],
                ['Gross Pay', f"{currency_symbol}{payslip_data['gross_pay']:.2f}"]
            ]
            
            earnings_table = Table(earnings_data, colWidths=[3.5*inch, 2.5*inch])
            earnings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            elements.append(earnings_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Deductions
            deductions_data = [
                ['DEDUCTIONS', 'Amount'],
                ['Total Deductions', f"{currency_symbol}{payslip_data['deductions']:.2f}"]
            ]
            
            deductions_table = Table(deductions_data, colWidths=[3.5*inch, 2.5*inch])
            deductions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(deductions_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Net pay
            net_data = [
                ['NET PAY', f"{currency_symbol}{payslip_data['net_pay']:.2f}"]
            ]
            
            net_table = Table(net_data, colWidths=[3.5*inch, 2.5*inch])
            net_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(net_table)
            
            # Build PDF
            doc.build(elements)
            return True
        
        except Exception as e:
            print(f"Error generating payslip PDF: {e}")
            return False


class HRManagerUI:
    """HR Manager User Interface"""
    
    def __init__(self, parent, db_connection, format_currency_func=None):
        self.parent = parent
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.analytics = HRAnalytics(db_connection)
        self.payslip_gen = HRPayslipGenerator(db_connection)
        self.format_currency = format_currency_func if format_currency_func else self._default_format_currency
        
        self.create_ui()
    
    def _default_format_currency(self, amount):
        """Default currency formatter if none provided"""
        try:
            self.cursor.execute("SELECT value FROM system_settings WHERE key = 'currency'")
            result = self.cursor.fetchone()
            currency_code = result[0] if result else 'GHS'
        except:
            currency_code = 'GHS'
        
        currency_symbols = {
            'USD': '$',
            'GHS': '₵',
            'NGN': '₦',
            'EUR': '€',
            'GBP': '£',
            'INR': '₹',
            'ZAR': 'R',
            'KES': 'KSh',
            'UGX': 'USh'
        }
        
        symbol = currency_symbols.get(currency_code, '₦')
        return f"{symbol}{amount:,.2f}"
    
    def create_ui(self):
        """Create the HR Manager UI"""
        # Create main frame with notebook (tabs)
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Employee Management Tab
        self.emp_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.emp_frame, text="👥 Employees")
        self.create_employee_management_tab()
        
        # Timesheet Tab
        self.timesheet_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.timesheet_frame, text="⏰ Timesheets")
        self.create_timesheet_tab()
        
        # Attendance Tab
        self.attendance_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.attendance_frame, text="✅ Attendance")
        self.create_attendance_tab()
        
        # Payslips Tab
        self.payslip_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.payslip_frame, text="💰 Payslips")
        self.create_payslips_tab()
        
        # Performance & Training Tab
        self.training_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.training_frame, text="🎯 Performance & Training")
        self.create_performance_training_tab()
        
        # AI Insights Tab
        self.ai_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(self.ai_frame, text="🤖 AI Insights")
        self.create_ai_insights_tab()
    
    def create_employee_management_tab(self):
        """Create employee management tab"""
        # Employee list frame
        list_frame = tk.Frame(self.emp_frame, bg='#f8f9fa')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(list_frame, text="Employees", font=('Segoe UI', 12, 'bold'), bg='#f8f9fa').pack()
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Employee listbox
        self.employee_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.employee_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.employee_listbox.yview)
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_employee_select)
        
        # Button frame
        btn_frame = tk.Frame(self.emp_frame, bg='#f8f9fa')
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        tk.Button(btn_frame, text="➕ Add Employee", command=self.add_employee_dialog, 
                 bg='#27ae60', fg='white', width=15).pack(pady=5)
        tk.Button(btn_frame, text="✏️ Edit Employee", command=self.edit_employee_dialog, 
                 bg='#3498db', fg='white', width=15).pack(pady=5)
        tk.Button(btn_frame, text="🗑️ Delete Employee", command=self.delete_employee, 
                 bg='#e74c3c', fg='white', width=15).pack(pady=5)
        tk.Button(btn_frame, text="� Import Teachers", command=self.import_teachers_from_main_db, 
                 bg='#9b59b6', fg='white', width=15).pack(pady=5)
        tk.Button(btn_frame, text="�🔄 Refresh", command=self.load_employees, 
                 bg='#95a5a6', fg='white', width=15).pack(pady=5)
        
        # Details frame
        details_frame = tk.LabelFrame(btn_frame, text="Employee Details", bg='#f8f9fa', font=('Segoe UI', 10, 'bold'))
        details_frame.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)
        
        self.emp_details_text = scrolledtext.ScrolledText(details_frame, height=15, width=30, bg='white')
        self.emp_details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.load_employees()
    
    def load_employees(self):
        """Load employees from database"""
        self.employee_listbox.delete(0, tk.END)
        
        try:
            self.cursor.execute("SELECT id, name, position, department FROM employees ORDER BY name")
            employees = self.cursor.fetchall()
            
            self.employees = {}
            for emp_id, name, position, department in employees:
                self.employees[name] = emp_id
                self.employee_listbox.insert(tk.END, f"{name} - {position}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {e}")
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.employee_listbox.curselection()
        if not selection:
            return
        
        employee_name = self.employee_listbox.get(selection[0])
        employee_id = self.employees.get(employee_name.split(' - ')[0])
        
        if employee_id:
            self.show_employee_details(employee_id)
    
    def show_employee_details(self, employee_id):
        """Show employee details in text widget"""
        self.emp_details_text.config(state=tk.NORMAL)
        self.emp_details_text.delete('1.0', tk.END)
        
        try:
            self.cursor.execute("""
                SELECT id, name, position, department, salary, email, phone, hire_date
                FROM employees WHERE id = ?
            """, (employee_id,))
            
            emp = self.cursor.fetchone()
            if emp:
                emp_id, name, position, department, salary, email, phone, hire_date = emp
                
                # Get performance score
                perf_score = self.analytics.calculate_employee_performance_score(employee_id)
                
                details = f"""NAME: {name}
POSITION: {position}
DEPARTMENT: {department}
SALARY: {self.format_currency(salary)}
EMAIL: {email}
PHONE: {phone}
HIRE DATE: {hire_date}

PERFORMANCE SCORE: {perf_score:.1f}/100
"""
                
                self.emp_details_text.insert(tk.END, details)
        
        except Exception as e:
            self.emp_details_text.insert(tk.END, f"Error loading details: {e}")
        
        self.emp_details_text.config(state=tk.DISABLED)
    
    def add_employee_dialog(self):
        """Show add employee dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Employee")
        dialog.geometry("400x500")
        
        # Create form
        fields = {
            'Name': tk.Entry(dialog),
            'Position': tk.Entry(dialog),
            'Department': tk.Entry(dialog),
            'Salary': tk.Entry(dialog),
            'Email': tk.Entry(dialog),
            'Phone': tk.Entry(dialog)
        }
        
        for i, (label, entry) in enumerate(fields.items()):
            tk.Label(dialog, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)
        
        def save_employee():
            try:
                self.cursor.execute("""
                    INSERT INTO employees (name, position, department, salary, email, phone, hire_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    fields['Name'].get(),
                    fields['Position'].get(),
                    fields['Department'].get(),
                    float(fields['Salary'].get()),
                    fields['Email'].get(),
                    fields['Phone'].get(),
                    date.today().isoformat()
                ))
                self.conn.commit()
                messagebox.showinfo("Success", "Employee added successfully")
                dialog.destroy()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add employee: {e}")
        
        tk.Button(dialog, text="Save", command=save_employee, bg='#27ae60', fg='white').grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        dialog.columnconfigure(1, weight=1)
    
    def edit_employee_dialog(self):
        """Show edit employee dialog"""
        selection = self.employee_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        messagebox.showinfo("Info", "Employee editing coming soon")
    
    def delete_employee(self):
        """Delete selected employee"""
        selection = self.employee_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            employee_name = self.employee_listbox.get(selection[0])
            employee_id = self.employees.get(employee_name.split(' - ')[0])
            
            try:
                self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Employee deleted")
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")
    
    def import_teachers_from_main_db(self):
        """Import teachers from main school database into HR employees table"""
        try:
            # Query teachers from the main database
            self.cursor.execute("""
                SELECT id, name, hire_date, starting_salary, qualifications, skills, phone, email
                FROM teachers
                ORDER BY name
            """)
            
            teachers = self.cursor.fetchall()
            
            if not teachers:
                messagebox.showinfo("Info", "No teachers found in the database")
                return
            
            imported_count = 0
            skipped_count = 0
            
            # Import each teacher
            for teacher_id, name, hire_date, salary, qualifications, skills, phone, email in teachers:
                try:
                    # Check if teacher already exists (by name and email)
                    self.cursor.execute("""
                        SELECT id FROM employees WHERE name = ? AND position = 'Teacher'
                    """, (name,))
                    
                    existing = self.cursor.fetchone()
                    
                    if existing:
                        # Update existing teacher record
                        self.cursor.execute("""
                            UPDATE employees
                            SET salary = ?, email = ?, phone = ?, hire_date = ?
                            WHERE id = ?
                        """, (salary or 0, email or '', phone or '', hire_date or date.today().isoformat(), existing[0]))
                        skipped_count += 1
                    else:
                        # Insert new teacher record
                        self.cursor.execute("""
                            INSERT INTO employees (name, position, department, salary, email, phone, hire_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (name, 'Teacher', 'Teaching Staff', salary or 0, email or '', phone or '', hire_date or date.today().isoformat()))
                        imported_count += 1
                
                except Exception as e:
                    print(f"Error importing teacher {name}: {e}")
                    continue
            
            self.conn.commit()
            
            # Show results
            message = f"""Teachers Import Complete!
            
✓ Newly imported: {imported_count}
⟳ Already exists (updated): {skipped_count}
━━━━━━━━━━━━━━━━━━━━
Total processed: {imported_count + skipped_count}"""
            
            messagebox.showinfo("Import Success", message)
            self.load_employees()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import teachers: {e}")
    
    def create_timesheet_tab(self):
        """Create timesheet management tab"""
        tk.Label(self.timesheet_frame, text="Timesheet Management", font=('Segoe UI', 12, 'bold'), 
                bg='#f8f9fa').pack(pady=10)
        
        # Timesheet controls
        control_frame = tk.Frame(self.timesheet_frame, bg='#f8f9fa')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(control_frame, text="Employee:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.ts_emp_var = tk.StringVar()
        ts_emp_combo = ttk.Combobox(control_frame, textvariable=self.ts_emp_var, width=20)
        ts_emp_combo.pack(side=tk.LEFT, padx=5)
        
        # Load employee names
        try:
            self.cursor.execute("SELECT name FROM employees ORDER BY name")
            emp_names = [row[0] for row in self.cursor.fetchall()]
            ts_emp_combo['values'] = emp_names
        except:
            pass
        
        tk.Label(control_frame, text="Month/Year:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.ts_month_var = tk.StringVar()
        self.ts_year_var = tk.StringVar()
        
        ts_month_spin = ttk.Spinbox(control_frame, from_=1, to=12, width=5, textvariable=self.ts_month_var)
        ts_month_spin.pack(side=tk.LEFT, padx=5)
        
        ts_year_spin = ttk.Spinbox(control_frame, from_=2020, to=2030, width=5, textvariable=self.ts_year_var)
        ts_year_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Load Timesheet", command=self.load_timesheet, 
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Save Timesheet", command=self.save_timesheet, 
                 bg='#27ae60', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Timesheet tree
        tree_frame = tk.Frame(self.timesheet_frame, bg='#f8f9fa')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.ts_tree = ttk.Treeview(tree_frame, columns=('date', 'hours', 'overtime'), height=15)
        self.ts_tree.heading('#0', text='Day')
        self.ts_tree.column('#0', width=100)
        self.ts_tree.heading('date', text='Date')
        self.ts_tree.column('date', width=100)
        self.ts_tree.heading('hours', text='Hours Worked')
        self.ts_tree.column('hours', width=100)
        self.ts_tree.heading('overtime', text='Overtime Hours')
        self.ts_tree.column('overtime', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ts_tree.config(yscrollcommand=scrollbar.set)
        self.ts_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to edit
        self.ts_tree.bind('<Double-1>', self.edit_timesheet_entry)
        
        # Summary frame
        summary_frame = tk.Frame(self.timesheet_frame, bg='#ecf0f1')
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.ts_summary_label = tk.Label(summary_frame, text="", font=('Segoe UI', 10),
                                         bg='#ecf0f1', justify=tk.LEFT)
        self.ts_summary_label.pack(anchor=tk.W, padx=10, pady=10)
        
        # Initialize with current month
        today = date.today()
        self.ts_month_var.set(today.month)
        self.ts_year_var.set(today.year)
    
    def edit_timesheet_entry(self, event):
        """Edit timesheet entry on double-click"""
        item = self.ts_tree.selection()[0]
        col = self.ts_tree.identify_column(event.x)
        
        # Only allow edit on hours (#2) and overtime (#3) columns
        if col not in ('#2', '#3'):
            return
        
        values = self.ts_tree.item(item, 'values')
        col_index = int(col[1:]) - 1
        
        if col_index >= len(values):
            return
        
        current_value = values[col_index]
        
        # Determine field name
        field_name = "Hours Worked" if col == '#2' else "Overtime Hours"
        
        # Simple popup for editing
        new_value = tk.simpledialog.askstring("Edit Entry", f"Enter {field_name}:", initialvalue=current_value)
        
        if new_value is not None:
            try:
                float(new_value)  # Validate it's a number
                new_values = list(values)
                new_values[col_index] = new_value
                self.ts_tree.item(item, values=new_values)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
    
    def save_timesheet(self):
        """Save timesheet data to database"""
        emp_name = self.ts_emp_var.get()
        if not emp_name:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        month = int(self.ts_month_var.get())
        year = int(self.ts_year_var.get())
        
        try:
            # Get employee ID
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            employee_id = emp_result[0]
            
            # Delete existing records for this month
            self.cursor.execute("""
                DELETE FROM timesheet_daily
                WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, month, year))
            
            # Insert new records
            total_hours = 0
            total_overtime = 0
            
            for item in self.ts_tree.get_children():
                values = self.ts_tree.item(item, 'values')
                date_str = values[0]
                hours = float(values[1]) if values[1] else 0
                overtime = float(values[2]) if values[2] else 0
                
                if hours > 0 or overtime > 0:
                    day = int(date_str.split('-')[-1])
                    self.cursor.execute("""
                        INSERT INTO timesheet_daily (employee_id, day, month, year, hours_worked, overtime_hours)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (employee_id, day, month, year, hours, overtime))
                    
                    total_hours += hours
                    total_overtime += overtime
            
            # Update or insert monthly summary
            self.cursor.execute("""
                SELECT id FROM timesheets WHERE employee_id = ? AND month = ? AND year = ?
            """, (employee_id, month, year))
            
            if self.cursor.fetchone():
                self.cursor.execute("""
                    UPDATE timesheets
                    SET hours_worked = ?, overtime_hours = ?
                    WHERE employee_id = ? AND month = ? AND year = ?
                """, (total_hours, total_overtime, employee_id, month, year))
            else:
                self.cursor.execute("""
                    INSERT INTO timesheets (employee_id, month, year, hours_worked, overtime_hours)
                    VALUES (?, ?, ?, ?, ?)
                """, (employee_id, month, year, total_hours, total_overtime))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Timesheet saved!\nTotal Hours: {total_hours}\nOvertime Hours: {total_overtime}")
            
            # Update summary
            self.update_timesheet_summary(total_hours, total_overtime)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save timesheet: {e}")
    
    def update_timesheet_summary(self, total_hours, total_overtime):
        """Update timesheet summary display"""
        expected_hours = 160  # Standard monthly hours
        variance = total_hours - expected_hours
        overtime_pay = total_overtime * (self.get_hourly_rate() * 1.5)
        
        summary_text = f"""MONTHLY SUMMARY:
  Total Hours Worked: {total_hours} hours (Expected: {expected_hours} hours)  Variance: {variance:+.1f} hours
  Overtime Hours: {total_overtime} hours  Estimated Overtime Pay: {self.format_currency(overtime_pay)}"""
        
        self.ts_summary_label.config(text=summary_text)
    
    def get_hourly_rate(self):
        """Get hourly rate for current employee"""
        emp_name = self.ts_emp_var.get()
        if not emp_name:
            return 0
        
        try:
            self.cursor.execute("SELECT salary FROM employees WHERE name = ?", (emp_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0] / 160  # Divide annual by 160 hours per month
            return 0
        except:
            return 0
    
    def load_timesheet(self):
        """Load timesheet data for selected employee and month"""
        emp_name = self.ts_emp_var.get()
        if not emp_name:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        month = int(self.ts_month_var.get())
        year = int(self.ts_year_var.get())
        
        try:
            # Get employee ID
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            employee_id = emp_result[0]
            
            # Clear existing tree
            self.ts_tree.delete(*self.ts_tree.get_children())
            
            # Get calendar for the month
            cal = calendar.monthcalendar(year, month)
            day_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            # Get existing timesheet data
            self.cursor.execute("""
                SELECT day, hours_worked, overtime_hours, leave_hours
                FROM timesheet_daily
                WHERE employee_id = ? AND month = ? AND year = ?
                ORDER BY day
            """, (employee_id, month, year))
            
            existing_data = {row[0]: row[1:] for row in self.cursor.fetchall()}
            
            # Populate tree with daily entries
            day_num = 1
            for week in cal:
                for day_of_week, day_date in enumerate(week):
                    if day_date == 0:
                        continue
                    
                    day_name_str = day_name[day_of_week]
                    date_str = f"{year}-{month:02d}-{day_date:02d}"
                    
                    if day_date in existing_data:
                        hours, overtime, leave = existing_data[day_date]
                    else:
                        hours, overtime, leave = 0, 0, 0
                    
                    self.ts_tree.insert('', tk.END, values=(
                        date_str,
                        hours,
                        overtime
                    ), text=f"{day_name_str} {day_date}")
                    
                    day_num += 1
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load timesheet: {e}")
    
    def create_attendance_tab(self):
        """Create attendance management tab"""
        tk.Label(self.attendance_frame, text="Employee Attendance", font=('Segoe UI', 12, 'bold'), 
                bg='#f8f9fa').pack(pady=10)
        
        # Attendance controls
        control_frame = tk.Frame(self.attendance_frame, bg='#f8f9fa')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(control_frame, text="Employee:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.att_emp_var = tk.StringVar()
        att_emp_combo = ttk.Combobox(control_frame, textvariable=self.att_emp_var, width=20)
        att_emp_combo.pack(side=tk.LEFT, padx=5)
        att_emp_combo.bind('<<ComboboxSelected>>', self.on_att_employee_select)
        
        # Load employee names
        try:
            self.cursor.execute("SELECT name FROM employees ORDER BY name")
            emp_names = [row[0] for row in self.cursor.fetchall()]
            att_emp_combo['values'] = emp_names
        except:
            pass
        
        tk.Label(control_frame, text="Date:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.att_date_var = tk.StringVar()
        self.att_date_var.set(date.today().isoformat())
        att_date_entry = tk.Entry(control_frame, textvariable=self.att_date_var, width=12)
        att_date_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Status:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.att_status_var = tk.StringVar()
        att_status_combo = ttk.Combobox(control_frame, textvariable=self.att_status_var, width=12, 
                                        values=['Present', 'Absent', 'Leave', 'Late'])
        att_status_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Save", command=self.save_attendance, 
                 bg='#27ae60', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Attendance records frame
        cal_frame = tk.Frame(self.attendance_frame, bg='#f8f9fa')
        cal_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(cal_frame, text="Attendance Records", font=('Segoe UI', 10, 'bold'), bg='#f8f9fa').pack()
        
        # Attendance tree
        self.att_tree = ttk.Treeview(cal_frame, columns=('date', 'status', 'notes'), height=15)
        self.att_tree.heading('#0', text='Date')
        self.att_tree.column('#0', width=100)
        self.att_tree.heading('date', text='Date')
        self.att_tree.column('date', width=100)
        self.att_tree.heading('status', text='Status')
        self.att_tree.column('status', width=100)
        self.att_tree.heading('notes', text='Notes')
        self.att_tree.column('notes', width=200)
        
        scrollbar = ttk.Scrollbar(cal_frame, orient=tk.VERTICAL, command=self.att_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.att_tree.config(yscrollcommand=scrollbar.set)
        self.att_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_payslips_tab(self):
        """Create payslips generation tab"""
        tk.Label(self.payslip_frame, text="Payslip Management", font=('Segoe UI', 12, 'bold'), 
                bg='#f8f9fa').pack(pady=10)
        
        control_frame = tk.Frame(self.payslip_frame, bg='#f8f9fa')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(control_frame, text="Employee:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.ps_emp_var = tk.StringVar()
        ps_emp_combo = ttk.Combobox(control_frame, textvariable=self.ps_emp_var, width=20)
        ps_emp_combo.pack(side=tk.LEFT, padx=5)
        
        # Load employee names
        try:
            self.cursor.execute("SELECT name FROM employees ORDER BY name")
            emp_names = [row[0] for row in self.cursor.fetchall()]
            ps_emp_combo['values'] = emp_names
        except:
            pass
        
        tk.Label(control_frame, text="Month/Year:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.ps_month_var = tk.StringVar()
        self.ps_year_var = tk.StringVar()
        
        ps_month_spin = ttk.Spinbox(control_frame, from_=1, to=12, width=5, textvariable=self.ps_month_var)
        ps_month_spin.pack(side=tk.LEFT, padx=5)
        
        ps_year_spin = ttk.Spinbox(control_frame, from_=2020, to=2030, width=5, textvariable=self.ps_year_var)
        ps_year_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Preview Payslip", command=self.preview_payslip, 
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Generate PDF", command=self.generate_payslip_pdf, 
                 bg='#27ae60', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Payslip display
        self.ps_text = scrolledtext.ScrolledText(self.payslip_frame, height=20, bg='white')
        self.ps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize
        today = date.today()
        self.ps_month_var.set(today.month)
        self.ps_year_var.set(today.year)
    
    def preview_payslip(self):
        """Preview payslip in text display"""
        emp_name = self.ps_emp_var.get()
        if not emp_name:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        month = int(self.ps_month_var.get())
        year = int(self.ps_year_var.get())
        
        try:
            # Get employee ID
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            employee_id = emp_result[0]
            
            # Calculate payslip
            payslip_data = self.payslip_gen.calculate_payslip(employee_id, month, year)
            if not payslip_data:
                messagebox.showerror("Error", "Failed to calculate payslip")
                return
            
            # Get currency symbol
            try:
                self.cursor.execute("SELECT value FROM system_settings WHERE key = 'currency'")
                result = self.cursor.fetchone()
                currency_code = result[0] if result else 'GHS'
            except:
                currency_code = 'GHS'
            
            currency_symbols = {
                'USD': '$',
                'GHS': '₵',
                'NGN': '₦',
                'EUR': '€',
                'GBP': '£',
                'INR': '₹',
                'ZAR': 'R',
                'KES': 'KSh',
                'UGX': 'USh'
            }
            
            currency_symbol = currency_symbols.get(currency_code, '₦')
            
            # Display payslip
            self.ps_text.config(state=tk.NORMAL)
            self.ps_text.delete('1.0', tk.END)
            
            payslip_text = f"""
{'='*60}
                        EMPLOYEE PAYSLIP
{'='*60}

Employee Name: {payslip_data['employee_name']}
Position: {payslip_data['position']}
Department: {payslip_data['department']}
Period: {payslip_data['month']}/{payslip_data['year']}

{'-'*60}
                        EARNINGS
{'-'*60}
Basic Pay:              {currency_symbol}{payslip_data['basic_pay']:>12,.2f}
Overtime Pay:           {currency_symbol}{payslip_data['overtime_pay']:>12,.2f}
Allowances:             {currency_symbol}{payslip_data['allowances']:>12,.2f}
────────────────────────────────────────────────
Gross Pay:              {currency_symbol}{payslip_data['gross_pay']:>12,.2f}

{'-'*60}
                        DEDUCTIONS
{'-'*60}
Total Deductions:       {currency_symbol}{payslip_data['deductions']:>12,.2f}

{'-'*60}
                        NET PAY
{'-'*60}
NET PAY:                {currency_symbol}{payslip_data['net_pay']:>12,.2f}

{'-'*60}
                    ATTENDANCE SUMMARY
{'-'*60}
Hours Worked:           {payslip_data['hours_worked']:>12,.1f} hrs
Overtime Hours:         {payslip_data['overtime_hours']:>12,.1f} hrs
Leave Hours:            {payslip_data['leave_hours']:>12,.1f} hrs

{'='*60}
"""
            
            self.ps_text.insert(tk.END, payslip_text)
            self.ps_text.config(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview payslip: {e}")
    
    def generate_payslip_pdf(self):
        """Generate payslip PDF with selected currency"""
        emp_name = self.ps_emp_var.get()
        if not emp_name:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        month = int(self.ps_month_var.get())
        year = int(self.ps_year_var.get())
        
        try:
            # Get employee ID
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            employee_id = emp_result[0]
            
            # Calculate payslip
            payslip_data = self.payslip_gen.calculate_payslip(employee_id, month, year)
            if not payslip_data:
                messagebox.showerror("Error", "Failed to calculate payslip")
                return
            
            # Get currency symbol
            try:
                self.cursor.execute("SELECT value FROM system_settings WHERE key = 'currency'")
                result = self.cursor.fetchone()
                currency_code = result[0] if result else 'GHS'
            except:
                currency_code = 'GHS'
            
            currency_symbols = {
                'USD': '$',
                'GHS': '₵',
                'NGN': '₦',
                'EUR': '€',
                'GBP': '£',
                'INR': '₹',
                'ZAR': 'R',
                'KES': 'KSh',
                'UGX': 'USh'
            }
            
            currency_symbol = currency_symbols.get(currency_code, '₦')
            
            # Get save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Payslip_{emp_name}_{month}_{year}.pdf"
            )
            
            if not file_path:
                return
            
            # Generate PDF with currency symbol
            success = self.payslip_gen.generate_pdf_payslip(payslip_data, file_path, currency_symbol)
            
            if success:
                messagebox.showinfo("Success", f"Payslip saved to:\n{file_path}")
            else:
                messagebox.showerror("Error", "Failed to generate PDF")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payslip: {e}")
    
    def save_attendance(self):
        """Save attendance record"""
        emp_name = self.att_emp_var.get()
        if not emp_name:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        att_date = self.att_date_var.get()
        status = self.att_status_var.get()
        
        if not status:
            messagebox.showwarning("Warning", "Please select a status")
            return
        
        try:
            # Get employee ID
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            employee_id = emp_result[0]
            
            # Insert attendance record
            self.cursor.execute("""
                INSERT OR REPLACE INTO employee_attendance (employee_id, attendance_date, status)
                VALUES (?, ?, ?)
            """, (employee_id, att_date, status))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Attendance recorded: {status}")
            
            # Refresh display
            self.load_attendance_records(employee_id)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {e}")
    
    def load_attendance_records(self, employee_id):
        """Load attendance records for employee"""
        try:
            self.att_tree.delete(*self.att_tree.get_children())
            
            self.cursor.execute("""
                SELECT attendance_date, status, notes
                FROM employee_attendance
                WHERE employee_id = ?
                ORDER BY attendance_date DESC
                LIMIT 30
            """, (employee_id,))
            
            for date_val, status, notes in self.cursor.fetchall():
                self.att_tree.insert('', tk.END, text=date_val, values=(date_val, status, notes or ''))
        
        except Exception as e:
            print(f"Error loading attendance: {e}")
    
    def on_att_employee_select(self, event):
        """Handle employee selection in attendance tab"""
        emp_name = self.att_emp_var.get()
        if not emp_name:
            return
        
        try:
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            emp_result = self.cursor.fetchone()
            if emp_result:
                self.load_attendance_records(emp_result[0])
        except Exception as e:
            print(f"Error selecting employee: {e}")
    
    def create_performance_training_tab(self):
        """Create performance and training tab"""
        tk.Label(self.training_frame, text="Performance & Training Management", font=('Segoe UI', 12, 'bold'), 
                bg='#f8f9fa').pack(pady=10)
        
        # Employee selection
        control_frame = tk.Frame(self.training_frame, bg='#f8f9fa')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(control_frame, text="Employee:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
        self.pt_emp_var = tk.StringVar()
        self.pt_emp_combo = ttk.Combobox(control_frame, textvariable=self.pt_emp_var, width=20)
        self.pt_emp_combo.pack(side=tk.LEFT, padx=5)
        self.pt_emp_combo.bind('<<ComboboxSelected>>', self.on_pt_employee_select)
        
        tk.Button(control_frame, text="Refresh", command=self.load_pt_employees, 
                 bg='#95a5a6', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Performance and training display
        self.pt_text = scrolledtext.ScrolledText(self.training_frame, height=20, bg='white')
        self.pt_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.load_pt_employees()
    
    def load_pt_employees(self):
        """Load employees for performance/training tab"""
        try:
            self.cursor.execute("SELECT name FROM employees ORDER BY name")
            names = [row[0] for row in self.cursor.fetchall()]
            self.pt_emp_combo['values'] = names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {e}")
    
    def on_pt_employee_select(self, event):
        """Handle employee selection in performance/training tab"""
        emp_name = self.pt_emp_var.get()
        
        try:
            self.cursor.execute("SELECT id FROM employees WHERE name = ?", (emp_name,))
            result = self.cursor.fetchone()
            
            if result:
                employee_id = result[0]
                self.show_performance_training_details(employee_id)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load details: {e}")
    
    def show_performance_training_details(self, employee_id):
        """Show performance and training details"""
        self.pt_text.config(state=tk.NORMAL)
        self.pt_text.delete('1.0', tk.END)
        
        try:
            # Get employee info
            self.cursor.execute("SELECT name FROM employees WHERE id = ?", (employee_id,))
            emp_name = self.cursor.fetchone()[0]
            
            # Get performance score
            perf_score = self.analytics.calculate_employee_performance_score(employee_id)
            
            # Get training needs
            training_needs = self.analytics.identify_training_needs(employee_id)
            
            # Get recommended actions
            actions = self.analytics.generate_recommended_actions(employee_id)
            
            details = f"""EMPLOYEE: {emp_name}
┌─────────────────────────────────────┐
│ PERFORMANCE SCORE: {perf_score:.1f}/100
└─────────────────────────────────────┘

TRAINING NEEDS:
═════════════════════════════════════
"""
            
            if training_needs:
                for need in training_needs:
                    details += f"""
Area: {need['area']}
Priority: {need['priority']}
Reason: {need['reason']}
───────────────────────────────────────"""
            else:
                details += "No training needs identified.\n"
            
            details += """

RECOMMENDED ACTIONS:
═════════════════════════════════════
"""
            
            if actions:
                for action in actions:
                    details += f"""
Action: {action['action']}
Description: {action['description']}
Urgency: {action['urgency']}
Due Date: {action['dueDate']}
───────────────────────────────────────"""
            else:
                details += "No recommended actions at this time.\n"
            
            self.pt_text.insert(tk.END, details)
        
        except Exception as e:
            self.pt_text.insert(tk.END, f"Error loading details: {e}")
        
        self.pt_text.config(state=tk.DISABLED)
    
    def create_ai_insights_tab(self):
        """Create AI insights tab"""
        tk.Label(self.ai_frame, text="AI-Powered HR Insights", font=('Segoe UI', 12, 'bold'), 
                bg='#f8f9fa').pack(pady=10)
        
        # Analysis type selection
        control_frame = tk.Frame(self.ai_frame, bg='#f8f9fa')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Button(control_frame, text="🎯 Overall Performance Analysis", command=self.show_overall_performance, 
                 bg='#3498db', fg='white', width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="📊 Department Analytics", command=self.show_dept_analytics, 
                 bg='#3498db', fg='white', width=30).pack(side=tk.LEFT, padx=5)
        
        # Insights display
        self.ai_text = scrolledtext.ScrolledText(self.ai_frame, height=20, bg='white')
        self.ai_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_overall_performance(self):
        """Show overall HR performance analysis"""
        self.ai_text.config(state=tk.NORMAL)
        self.ai_text.delete('1.0', tk.END)
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM employees")
            total_emp = self.cursor.fetchone()[0]
            
            analysis = f"""╔═══════════════════════════════════════════════╗
║     OVERALL HR PERFORMANCE ANALYSIS           ║
╚═══════════════════════════════════════════════╝

Total Employees: {total_emp}

PERFORMANCE DISTRIBUTION:
─────────────────────────────────────────────

"""
            
            # Calculate performance distribution
            high_performers = 0
            medium_performers = 0
            low_performers = 0
            
            self.cursor.execute("SELECT id FROM employees")
            for emp_id, in self.cursor.fetchall():
                score = self.analytics.calculate_employee_performance_score(emp_id)
                if score >= 80:
                    high_performers += 1
                elif score >= 60:
                    medium_performers += 1
                else:
                    low_performers += 1
            
            analysis += f"""
High Performers (80+): {high_performers} ({high_performers/max(total_emp,1)*100:.1f}%)
Medium Performers (60-79): {medium_performers} ({medium_performers/max(total_emp,1)*100:.1f}%)
Low Performers (<60): {low_performers} ({low_performers/max(total_emp,1)*100:.1f}%)

RECOMMENDATIONS:
─────────────────────────────────────────────
1. Recognize and incentivize high performers
2. Provide targeted training for medium performers
3. Schedule performance improvement plans for low performers
"""
            
            self.ai_text.insert(tk.END, analysis)
        
        except Exception as e:
            self.ai_text.insert(tk.END, f"Error: {e}")
        
        self.ai_text.config(state=tk.DISABLED)
    
    def show_dept_analytics(self):
        """Show comprehensive department analytics"""
        self.ai_text.config(state=tk.NORMAL)
        self.ai_text.delete('1.0', tk.END)
        
        try:
            analysis = """╔═══════════════════════════════════════════════════════════╗
║         DEPARTMENT ANALYTICS & INSIGHTS REPORT           ║
╚═══════════════════════════════════════════════════════════╝\n
"""
            
            # Get all unique departments
            self.cursor.execute("SELECT DISTINCT department FROM employees ORDER BY department")
            departments = [row[0] for row in self.cursor.fetchall()]
            
            if not departments:
                analysis += "No departments found in the system."
                self.ai_text.insert(tk.END, analysis)
                self.ai_text.config(state=tk.DISABLED)
                return
            
            # Department summary metrics
            dept_metrics = []
            
            for dept in departments:
                # Get employee count
                self.cursor.execute(
                    "SELECT COUNT(*) FROM employees WHERE department = ?", (dept,)
                )
                emp_count = self.cursor.fetchone()[0] or 0
                
                # Get salary info
                self.cursor.execute(
                    "SELECT AVG(salary), SUM(salary), MIN(salary), MAX(salary) FROM employees WHERE department = ?",
                    (dept,)
                )
                salary_data = self.cursor.fetchone()
                avg_salary = salary_data[0] or 0
                total_salary = salary_data[1] or 0
                min_salary = salary_data[2] or 0
                max_salary = salary_data[3] or 0
                
                # Get attendance rate
                self.cursor.execute("""
                    SELECT CAST(SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
                           NULLIF(COUNT(*), 0) * 100
                    FROM employee_attendance a
                    JOIN employees e ON a.employee_id = e.id
                    WHERE e.department = ? AND a.date >= date('now', '-30 days')
                """, (dept,))
                
                attendance_result = self.cursor.fetchone()
                attendance_rate = attendance_result[0] if attendance_result and attendance_result[0] else 0
                
                # Calculate performance scores for department
                self.cursor.execute("SELECT id FROM employees WHERE department = ?", (dept,))
                emp_ids = [row[0] for row in self.cursor.fetchall()]
                
                perf_scores = []
                for emp_id in emp_ids:
                    score = self.analytics.calculate_employee_performance_score(emp_id)
                    perf_scores.append(score)
                
                avg_perf = sum(perf_scores) / len(perf_scores) if perf_scores else 0
                
                # Count high/medium/low performers
                high_perf = sum(1 for s in perf_scores if s >= 80)
                medium_perf = sum(1 for s in perf_scores if 60 <= s < 80)
                low_perf = sum(1 for s in perf_scores if s < 60)
                
                # Get training needs count
                training_needed = 0
                for emp_id in emp_ids:
                    needs = self.analytics.identify_training_needs(emp_id)
                    training_needed += len(needs)
                
                dept_metrics.append({
                    'name': dept,
                    'emp_count': emp_count,
                    'avg_salary': avg_salary,
                    'total_salary': total_salary,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'avg_perf': avg_perf,
                    'high_perf': high_perf,
                    'medium_perf': medium_perf,
                    'low_perf': low_perf,
                    'attendance': attendance_rate,
                    'training_needs': training_needed,
                    'emp_ids': emp_ids
                })
            
            # Generate report for each department
            for metric in dept_metrics:
                analysis += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEPARTMENT: {metric['name'].upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STAFFING:
  Total Employees: {metric['emp_count']}
  
PERFORMANCE DISTRIBUTION:
  Average Score: {metric['avg_perf']:.1f}/100
  High Performers (80+): {metric['high_perf']} ({metric['high_perf']/max(metric['emp_count'],1)*100:.0f}%)
  Medium Performers (60-79): {metric['medium_perf']} ({metric['medium_perf']/max(metric['emp_count'],1)*100:.0f}%)
  Low Performers (<60): {metric['low_perf']} ({metric['low_perf']/max(metric['emp_count'],1)*100:.0f}%)
  
ATTENDANCE:
  Monthly Average: {metric['attendance']:.1f}%
  Status: {'✓ Excellent' if metric['attendance'] >= 95 else '○ Satisfactory' if metric['attendance'] >= 85 else '✗ Needs Improvement'}

PAYROLL:
  Average Salary: {self.format_currency(metric['avg_salary'])}
  Total Payroll: {self.format_currency(metric['total_salary'])}
  Salary Range: {self.format_currency(metric['min_salary'])} - {self.format_currency(metric['max_salary'])}
  
TRAINING & DEVELOPMENT:
  Training Needs Identified: {metric['training_needs']}
  Employees Requiring Training: {len([e for e in metric['emp_ids'] if self.analytics.identify_training_needs(e)])}
  
"""
                
                # Generate recommendations
                analysis += "RECOMMENDATIONS:\n"
                
                if metric['avg_perf'] < 70:
                    analysis += "  ⚠️  Department performance below target. Implement training program.\n"
                elif metric['avg_perf'] >= 85:
                    analysis += "  ✓ Strong department performance. Consider recognition program.\n"
                
                if metric['low_perf'] > 0:
                    analysis += f"  ⚠️  {metric['low_perf']} low performers need improvement plans.\n"
                
                if metric['attendance'] < 85:
                    analysis += "  ⚠️  Attendance rate below standard (85%). Address absenteeism.\n"
                
                if metric['training_needs'] > metric['emp_count'] / 2:
                    analysis += "  ⚠️  High training needs. Schedule training sessions.\n"
                
                if metric['emp_count'] == 0:
                    analysis += "  ℹ️  No employees in this department.\n"
                
                analysis += "\n"
            
            # Summary statistics
            total_emp = sum(m['emp_count'] for m in dept_metrics)
            avg_dept_perf = sum(m['avg_perf'] * m['emp_count'] for m in dept_metrics) / max(total_emp, 1)
            total_payroll = sum(m['total_salary'] for m in dept_metrics)
            avg_attendance = sum(m['attendance'] for m in dept_metrics) / len(dept_metrics) if dept_metrics else 0
            
            analysis += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ORGANIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Employees: {total_emp}
Total Departments: {len(dept_metrics)}
Overall Performance: {avg_dept_perf:.1f}/100
Total Payroll: {self.format_currency(total_payroll)}
Average Attendance: {avg_attendance:.1f}%

TOP PERFORMING DEPARTMENT:
  {max(dept_metrics, key=lambda x: x['avg_perf'])['name'].upper()} ({max(dept_metrics, key=lambda x: x['avg_perf'])['avg_perf']:.1f}/100)

DEPARTMENT WITH MOST TRAINING NEEDS:
  {max(dept_metrics, key=lambda x: x['training_needs'])['name'].upper()} ({max(dept_metrics, key=lambda x: x['training_needs'])['training_needs']} needs)

STRATEGIC RECOMMENDATIONS:
  1. Focus on departments with low performance scores
  2. Implement cross-department knowledge sharing
  3. Schedule quarterly training for high-need areas
  4. Monitor attendance trends closely
  5. Recognize top-performing departments with incentives
"""
            
            self.ai_text.insert(tk.END, analysis)
        
        except Exception as e:
            self.ai_text.insert(tk.END, f"Error loading department analytics: {str(e)}\n")
            import traceback
            self.ai_text.insert(tk.END, traceback.format_exc())
        
        self.ai_text.config(state=tk.DISABLED)


def create_hr_manager_ui(parent_frame, db_connection, format_currency_func=None):
    """Create HR Manager UI embedded in parent frame"""
    ui = HRManagerUI(parent_frame, db_connection, format_currency_func)
    return ui
