# Copilot Instructions for Gaybeck Starkids SMS

## Project Overview
- Python/Tkinter-based school management system with AI analytics, real-time sync, and role-based access.
- Main entry: `sms.py`. Core modules: student, teacher, attendance, fee, grading, financial, and AI insights.
- Database: SQLite3 (`database/school_management.db`). Backups in `backups/` and `database_backups/`.

## Architecture & Data Flow
- UI: Tkinter forms, scrollable interfaces, and calendar widgets (see `DATE_PICKER_SCROLLABLE_FORMS_DOCUMENTATION.md`).
- Real-time sync: `comprehensive_sync_system.py`, `realtime_sync.py` (docs: `COMPREHENSIVE_SYNC_DOCUMENTATION.md`).
- Database relationships: `incremental_relationships.py` sets up foreign keys and triggers.
- AI: Machine learning (scikit-learn, pandas, numpy) for risk analysis and predictive reports.
- Role-based access: Admin, Teacher, Accountant (see `USER_MANAGEMENT_GUIDE.md`).

## Developer Workflows
- **Install:** Use `install_dependencies.bat` or `pip install -r requirements.txt`.
- **Run:** `python sms.py` (Windows, Python 3.13+ only; avoid 3.14 due to Tkinter issues).
- **Database setup:** Run `incremental_relationships.py` and `comprehensive_sync_system.py` if initializing.
- **Backups:** Use built-in menu (Admin) or copy files from `backups/`.
- **Testing:** Place scripts in `tests/`. No automated test runner; run manually.
- **Dev scripts:** Maintenance/optimization in `dev-scripts/` (see file names for purpose).

## Conventions & Patterns
- All user roles and permissions managed via UI and database (see `USER_MANAGEMENT_GUIDE.md`).
- Grade validation: 0-100 enforced in UI and backend.
- AI features require optional packages; check for import errors if disabled.
- Responsive design: Target 1366x768+; scrollable forms for smaller screens.
- Database triggers ensure sync between fee, attendance, and financial modules.
- Code and database backups use timestamped filenames.

## Integration Points
- External: scikit-learn, pandas, numpy, tkcalendar, reportlab, pillow, opencv-python.
- All integration scripts and fixes in `dev-scripts/`.
- Documentation for major features in `docs/` (see file list above).

## Examples
- To add a new module, follow patterns in `sms.py` and sync logic in `comprehensive_sync_system.py`.
- For new database tables, update `incremental_relationships.py` and ensure triggers for sync.
- For UI changes, use scrollable forms and DateEntry widgets as in documented guides.

## Key Files & Directories
- `sms.py`: Main app logic and UI
- `database/`: SQLite DB
- `dev-scripts/`: Maintenance/optimization
- `docs/`: Feature documentation
- `backups/`, `database_backups/`: Backup files
- `tests/`: Manual test scripts

---
For unclear patterns or missing documentation, check `/docs` or ask for clarification.
