# School Management System (DeepSeek SMS)

Comprehensive application documentation for stakeholder review.

Last updated: October 26, 2025

---

## 1) Executive Summary

DeepSeek SMS is a desktop School Management System built with Python (Tkinter) and SQLite that centralizes student, class, attendance, fees, teachers, and finance management. The system includes a real-time synchronization layer for audit logging, dashboard metrics, statistics caching, and notification handling. The application is production-ready for single-site deployments on Windows.

Key capabilities:
- Student, teacher, class, promotions management
- Fees management with arrears tracking and payment dates
- Financial management (categories, income/expense transactions, reports)
- Attendance tracking and analytics
- Role-based access control (users with roles and permissions)
- Real-time sync: activity logs, statistics cache, views, and notifications

---

## 2) Architecture Overview

- UI Layer: Tkinter application (`sms.py`) with multi-tab workflows for students, fees, finance, attendance, dashboards, and reports.
- Data Layer: SQLite database (`school_management.db`, also `school.db` present). Tables are created on first run if missing.
- Sync & Analytics Layer: Incremental relationships, triggers, and reporting views (`incremental_relationships.py`, `comprehensive_sync_system.py`, `realtime_sync.py`).

Data flow highlights:
- Fees entered/updated in `fees` table feed financial analytics and arrears reporting.
- Financial transactions in `financial_transactions` power real-time income/expense summaries.
- Triggers and views maintain live statistics and activity logs for dashboards.

---

## 3) Modules and Responsibilities

- `sms.py`: Main application. Creates tables, defines UI, handles CRUD for students, teachers, fees, attendance, finances, and reporting. Also seeds defaults and loads dashboards.
- `incremental_relationships.py`: Adds audit tables, triggers, and real-time analytical views. Initializes statistics caching and sync status.
- `comprehensive_sync_system.py`: Adds additional triggers and views, and can backfill/synchronize data where necessary. Focused on broader real-time sync across modules and notification rules.
- `realtime_sync.py`: Programmatic sync manager. Provides helper APIs to log user activity, create notifications, maintain statistics cache, and query dashboard/analytics views. Also includes a background monitoring loop.

Support folders:
- `docs/`: All documentation and guides.
- `dev-scripts/`: Development utilities, fix/verify scripts (not required at runtime).
- `backups/`: Code and database backups for recovery.
- `reports/`: Audit and system reports.

---

## 4) Database Schema (Current Key Tables)

Created by `sms.py` on startup if missing:

- `classes(id, class_name, capacity)`
- `students(id, student_id, name, date_of_birth, gender, date_of_admission, class_id, previous_class_id, father_name, mother_name, phone, address, parent_email, emergency_* fields, medical_allergies, document_path, transportation, bus_fee, feeding_fee_paid, monthly_fee, ...)`
- `teachers(id, name, hire_date, class_id, starting_salary, qualifications, skills, document_path, phone, email, created_date)`
- `fees(id, student_id, month, year, amount_due, amount_paid, arrears, feeding_fee_paid, bus_fee_paid, payment_date)`
- `attendance(id, student_id, date, present, feeding_fee_paid, bus_fee_paid)`
- `promotions(id, student_id, from_class_id, to_class_id, promotion_date, academic_year)`
- `users(id, username, password, full_name, role, email, phone, permissions, is_active, created_date, last_login)`
- `financial_categories(id, category_name, category_type[income|expense], description, is_active, created_date)`
- `financial_transactions(id, transaction_date, category_id, transaction_type[income|expense], amount, description, reference_number, payment_method, created_by, notes, created_date)`
- `budget_plans(id, plan_name, category_id, budgeted_amount, period_type, start_date, end_date, is_active, created_date)`
- `financial_reports(id, report_name, report_type, generated_date, date_from, date_to, total_income, total_expenses, net_profit, generated_by, file_path)`

Added by `incremental_relationships.py` (supporting infra):
- `user_activity_log(id, user_id, username, action_type, table_affected, record_id, old_values, new_values, timestamp, ip_address, session_id, details)`
- `system_notifications(id, user_id, title, message, notification_type, is_read, created_at, expires_at, action_url, priority)`
- `sync_status(id, table_name, last_sync_timestamp, sync_count, status, last_error, auto_sync_enabled)`
- `statistics_cache(id, metric_name UNIQUE, metric_value, metric_data, calculated_at, expires_at, category)`

Views (analytics, reporting):
- `dashboard_stats(metric, value, calculated_at)` – high-level KPIs (students, classes, teachers, monthly income/expenses, etc.)
- `student_performance(...)` – attendance-based performance per student
- `financial_summary(...)` – category-level transaction summaries
- `class_analytics(...)` – per-class analytics
- `recent_activities(source, username, activity, entity, timestamp, details)` – merged feed of user activity and notifications

Note: Foreign keys are present where supported; `PRAGMA foreign_keys=ON` is used within scripts.

---

## 5) Real-time Synchronization & Analytics

There are two mechanisms working together:

1) Database-level triggers and views (`incremental_relationships.py`, `comprehensive_sync_system.py`)
- Log student updates and fee payment changes to `user_activity_log`.
- Maintain `statistics_cache` for quick metrics (attendance, enrollments, income/expense, etc.).
- Create real-time analytical views consumed by UI and APIs.
- Generate notifications for important thresholds (e.g., high arrears as configured in triggers).

2) Programmatic sync manager (`realtime_sync.py`)
- Log activity on demand via `log_activity()` helpers.
- Create system notifications via `notify_system()`.
- Update cached metrics via `update_metric()`.
- Fetch dashboard, student, financial, class analytics with `get_*` helpers.
- Optional background task that refreshes stats and performs cleanup.

---

## 6) Core Functional Areas

- Students: Register/manage students, class assignment, promotions, contact/emergency data, transport options.
- Teachers: Manage teacher profiles, assignments, and contact info.
- Fees: Record dues and payments, compute arrears, mark feeding/bus flags, store payment dates.
- Attendance: Daily tracking with statistics and recent trend analysis (via views and sync manager).
- Financials: Categories (e.g., School Fees), income & expense transactions, quick actions, and reports.
- Dashboard & Reports: Aggregated KPIs and insights via `dashboard_stats`, `financial_summary`, and `class_analytics`.
- Users & Roles: Auth scaffolding; roles stored in `users.role` with optional granular permissions field.

---

## 7) Data Flows of Interest

- Fee Management → Financial Analytics:
  - Payments are recorded in `fees.amount_paid` with `payment_date` and rolling `arrears`.
  - System reports and dashboard pull totals from `fees` and `financial_transactions` (where applicable) and analytical views.

- Attendance → Dashboard KPIs:
  - Insert/update on `attendance` updates `statistics_cache` via triggers and feeds `dashboard_stats`.

- User Operations → Audit & Notifications:
  - Inserts/updates are logged to `user_activity_log` (with old/new values), and relevant notifications appear in `system_notifications`.

---

## 8) Setup & Run (Windows / PowerShell)

From the project root:

```powershell
# 1) (Optional) Install tkcalendar for date picker widgets
pip install tkcalendar

# 2) Initialize relationships, triggers, and views
python .\incremental_relationships.py
python .\comprehensive_sync_system.py

# 3) Launch the application
python .\sms.py
```

Database files used by default:
- `school_management.db` (primary)
- `school.db` (legacy/alternate)

> Note: The application creates missing tables on first run.

---

## 9) Roles, Permissions, and Security Notes

- Users table includes role (e.g., admin, finance, teacher, viewer) and optional `permissions` field to support fine-grained access.
- Suggested practice: Hash passwords (current schema stores plain text; consider upgrading to a hashed approach using `bcrypt`).
- Enable `PRAGMA foreign_keys = ON` consistently to enforce referential integrity.
- Backups are stored under `/backups` with timestamps. Recommended to automate periodic DB backups.

---

## 10) Testing Guidance (Manual QA Checklist)

Functional checks:
- Students
  - Create, edit, and reassign student to classes; confirm in `students` and dashboards.
- Fees
  - Add fee record with payment; confirm `amount_paid`, `arrears`, and `payment_date` show correctly.
  - Verify fee totals and monthly summaries in dashboards/reports.
- Financials
  - Add income/expense transaction; verify appearance in transaction lists and `financial_summary` view.
- Attendance
  - Mark present/absent for today; confirm `today_attendance_rate` metric updates.
- Notifications & Activity
  - Perform updates; check `recent_activities` view and `system_notifications` records.

Optional data integrity checks:
- Ensure `arrears = max(0, amount_due - amount_paid)` is respected across updates.
- Spot-check foreign-key relationships by deleting a parent record and validating behavior.

---

## 11) Maintenance & Operations

- Data backups: keep automated copies in `/backups`.
- Cleanup tasks: `realtime_sync.py` offers `cleanup_old_data()` for logs/notifications/statistics.
- Performance: heavy aggregations are cached in `statistics_cache`; ensure triggers remain performant.
- Monitoring: use `sync_status` to check when each table last updated and how often.

---

## 12) Known Limitations & Suggestions

- Password hashing not yet enforced – prioritize `bcrypt` integration.
- Unit tests are not present – consider adding a small test suite for core flows.
- Some views refer to optional/extended tables (e.g., `tests`, `homework`, `student_remarks`); these are safe but may be no-op if tables aren’t present.
- If multiple databases are used (`school.db` vs `school_management.db`), standardize and migrate data to a single source of truth.

---

## 13) Directory Map (Tidied)

```
DEEPSEEK SMS/
├── sms.py
├── incremental_relationships.py
├── comprehensive_sync_system.py
├── realtime_sync.py
├── school_management.db
├── school.db
├── requirements.txt
├── README.md
├── docs/
│   ├── APPLICATION_COMPREHENSIVE_REVIEW.md (this file)
│   ├── COMPREHENSIVE_SYNC_DOCUMENTATION.md
│   ├── DATE_PICKER_SCROLLABLE_FORMS_DOCUMENTATION.md
│   ├── USER_MANAGEMENT_GUIDE.md
│   └── ...
├── backups/
├── dev-scripts/
└── reports/
```

---

## 14) Roadmap (Proposed Next Steps)

- Security: hash passwords, add login throttling, role-based control guards in UI handlers.
- Financials: tighter linkage between fees and `financial_transactions` if business rules require mirroring; add reconciliation reports.
- Testing: introduce pytest-based regression tests for fees, attendance, and financial dashboards.
- UX: add search/filtering across all list views; export to CSV/PDF.
- Deployment: bundle as a Windows executable (PyInstaller) and provide installer.

---

## 15) Appendix: Operational SQL References

- Fees totals by month:
```sql
SELECT strftime('%Y-%m', payment_date) AS ym, SUM(amount_paid)
FROM fees
GROUP BY ym
ORDER BY ym DESC;
```

- Income vs Expenses (current month):
```sql
SELECT transaction_type, SUM(amount)
FROM financial_transactions
WHERE strftime('%Y-%m', transaction_date) = strftime('%Y-%m', date('now'))
GROUP BY transaction_type;
```

- Recent activities (last 100):
```sql
SELECT * FROM recent_activities ORDER BY timestamp DESC LIMIT 100;
```

---

This document summarizes the system as currently implemented in the repository and database. It is suitable for stakeholder review and technical onboarding.
