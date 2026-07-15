# Gaybeck Starkids SMS Architecture

## Overview
The system is a desktop-first school management platform with optional web APIs and AI-enhanced services.

Core layers:
- Presentation: Tkinter desktop UI in sms.py and supporting UI modules.
- Domain services: attendance, fees, grading, HR, notifications, AI tutoring, EWS.
- Data layer: SQLite database with views, triggers, and sync helpers.
- Operations: backup automation, validation, logging, test-data seeding, deployment scripts.

## Runtime Components
- Desktop application: sms.py
- Web backend: web_app/backend/app.py (Flask)
- Sync and activity/audit logging: realtime_sync.py
- Backup and restore automation: backup_manager.py
- Validation framework: input_validation.py
- Error and performance monitoring: error_handling.py

## Data Architecture
Primary database:
- database/school_management.db (or local school_management.db fallback)

Storage folders:
- database_backups/: automated and manual backup artifacts
- restore_points/: pre-restore and startup restore points
- logs/: rotating application logs

Key behavior:
- Relational schema with foreign keys.
- Activity and notification tables provide operational traceability.
- performance_metrics stores operation latency and execution status.

## Security and Environment
- Flask production mode is controlled by environment-selected config class.
- Production config disables debug and testing flags.
- Secrets are expected through environment variables (SECRET_KEY, JWT_SECRET_KEY).
- Biometric features degrade gracefully when optional dependencies are unavailable.

## Reliability and Operations
- Daily automated backups target 02:00 local time.
- Scheduler uses schedule package when present, with internal fallback scheduler otherwise.
- Startup restore points provide fast rollback options before runtime mutations.
- Validation utilities enforce data quality for student, teacher, and financial workflows.

## Testing Strategy
- Baseline integration checks: test_comprehensive.py, test_extended.py, test_phase2_integration.py.
- Deployment validation: test_deployment_readiness.py, verify_installation.py.
- Seeding support: seed_test_data.py with threshold-based if-empty mode.

## Extension Points
- New AI features should attach to service modules and expose UI through component frames.
- New operational metrics should be written to performance_metrics with operation name and duration.
- New sensitive workflows should log activity through realtime_sync.log_user_activity.
