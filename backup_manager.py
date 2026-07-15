"""
Automated Database Backup Manager
Provides scheduled and manual backup functionality for SMS database
Version: 1.0.0
"""

import os
import shutil
import sqlite3
import logging
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

# Try to import schedule, make it optional
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False

logger = logging.getLogger(__name__)

class DatabaseBackupManager:
    """Manages automated and manual database backups"""
    
    def __init__(self, db_path='school_management.db', backup_dir='database_backups', max_backups=30, restore_dir='restore_points'):
        """
        Initialize backup manager
        
        Args:
            db_path: Path to the database file
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep (older ones deleted)
            restore_dir: Directory to store restore points
        """
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        self.restore_dir = restore_dir
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        os.makedirs(restore_dir, exist_ok=True)
        
        logger.info(f"BackupManager initialized: {db_path} → {backup_dir}")
    
    def create_backup(self, description=""):
        """
        Create a manual backup of the database
        
        Args:
            description: Optional description for the backup
            
        Returns:
            Path to the backup file, or None if failed
        """
        if not os.path.exists(self.db_path):
            logger.error(f"Database file not found: {self.db_path}")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"school_db_backup_{timestamp}.db"
            if description:
                backup_name = f"school_db_backup_{timestamp}_{description.replace(' ', '_')}.db"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Create backup using SQLite backup API
            source_conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_path)
            
            with backup_conn:
                source_conn.backup(backup_conn)
            
            backup_conn.close()
            source_conn.close()
            
            size_kb = os.path.getsize(backup_path) / 1024
            logger.info(f"✅ Backup created: {backup_name} ({size_kb:.1f} KB)")
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {str(e)}")
            return None
    
    def _cleanup_old_backups(self):
        """Remove old backups, keeping only max_backups most recent"""
        try:
            backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith('school_db_backup_') and f.endswith('.db')],
                key=lambda f: os.path.getctime(os.path.join(self.backup_dir, f)),
                reverse=True
            )
            
            if len(backups) > self.max_backups:
                for old_backup in backups[self.max_backups:]:
                    backup_path = os.path.join(self.backup_dir, old_backup)
                    os.remove(backup_path)
                    logger.info(f"Deleted old backup: {old_backup}")
                    
        except Exception as e:
            logger.error(f"Error during backup cleanup: {str(e)}")
    
    def restore_backup(self, backup_path):
        """
        Restore database from a backup
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        try:
            # Create a restore point from current database
            restore_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            restore_path = os.path.join(self.restore_dir, f"pre_restore_{restore_timestamp}.db")
            shutil.copy2(self.db_path, restore_path)
            logger.info(f"Pre-restore backup created: {restore_path}")
            
            # Restore from backup
            backup_conn = sqlite3.connect(backup_path)
            restore_conn = sqlite3.connect(self.db_path)
            
            with restore_conn:
                backup_conn.backup(restore_conn)
            
            restore_conn.close()
            backup_conn.close()
            
            logger.info(f"✅ Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {str(e)}")
            return False

    def create_restore_point(self, reason="startup"):
        """Create a lightweight restore point copy of the active database."""
        if not os.path.exists(self.db_path):
            logger.error(f"Database file not found for restore point: {self.db_path}")
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_reason = (reason or "manual").replace(" ", "_")
            restore_name = f"restore_point_{timestamp}_{safe_reason}.db"
            restore_path = os.path.join(self.restore_dir, restore_name)
            shutil.copy2(self.db_path, restore_path)
            logger.info(f"✅ Restore point created: {restore_name}")
            return restore_path
        except Exception as e:
            logger.error(f"❌ Restore point creation failed: {str(e)}")
            return None
    
    def get_backup_list(self):
        """Get list of available backups with metadata"""
        backups = []
        try:
            for filename in sorted(os.listdir(self.backup_dir), reverse=True):
                if filename.startswith('school_db_backup_') and filename.endswith('.db'):
                    filepath = os.path.join(self.backup_dir, filename)
                    size_kb = os.path.getsize(filepath) / 1024
                    mtime = datetime.fromtimestamp(os.path.getctime(filepath))
                    backups.append({
                        'name': filename,
                        'path': filepath,
                        'size': f"{size_kb:.1f} KB",
                        'created': mtime.strftime("%Y-%m-%d %H:%M:%S")
                    })
        except Exception as e:
            logger.error(f"Error listing backups: {str(e)}")
        
        return backups
    
    def list_backups(self):
        """Alias for get_backup_list for backward compatibility"""
        backups = self.get_backup_list()
        return [(b['name'], b['size'].split()[0], b['created']) for b in backups]
    
    def verify_backup(self, backup_path):
        """Verify backup integrity"""
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()
            
            if table_count > 30:
                logger.info(f"✅ Backup verified: {table_count} tables")
                return True
            else:
                logger.warning(f"⚠️ Backup may be incomplete: {table_count} tables")
                return False
                
        except Exception as e:
            logger.error(f"❌ Backup verification failed: {str(e)}")
            return False


class BackupScheduler:
    """Manages scheduled backups"""
    
    def __init__(self, backup_manager, backup_time="02:00"):
        """
        Initialize backup scheduler
        
        Args:
            backup_manager: BackupManager instance
            backup_time: Time for daily backups (format: "HH:MM")
        """
        self.backup_manager = backup_manager
        self.backup_time = backup_time
        self.scheduler_thread = None
        self.is_running = False
        self.last_backup_date = None
        
        if SCHEDULE_AVAILABLE:
            logger.info(f"BackupScheduler configured for {backup_time} daily backups")
        else:
            logger.warning("Schedule package not available. Using internal scheduler fallback.")
    
    def start(self):
        """Start the backup scheduler in background"""
        if self.is_running:
            logger.warning("Scheduler already running")
            return
        
        self.is_running = True
        
        if SCHEDULE_AVAILABLE:
            # Schedule daily backup
            schedule.every().day.at(self.backup_time).do(self._scheduled_backup)
        
        # Start scheduler in background thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info(f"✅ Backup scheduler started (daily at {self.backup_time})")
    
    def stop(self):
        """Stop the backup scheduler"""
        self.is_running = False
        if SCHEDULE_AVAILABLE:
            schedule.clear()
        logger.info("Backup scheduler stopped")
    
    def _scheduled_backup(self):
        """Perform scheduled backup"""
        logger.info("Running scheduled daily backup...")
        backup_path = self.backup_manager.create_backup(description="automated")
        if backup_path:
            self.backup_manager.verify_backup(backup_path)
    
    def _run_scheduler(self):
        """Run scheduler loop"""
        while self.is_running:
            try:
                if SCHEDULE_AVAILABLE:
                    schedule.run_pending()
                else:
                    now = datetime.now()
                    current_hhmm = now.strftime("%H:%M")
                    if current_hhmm == self.backup_time and self.last_backup_date != now.date():
                        self._scheduled_backup()
                        self.last_backup_date = now.date()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(60)


def get_backup_manager(db_path='school_management.db', backup_dir='database_backups', max_backups=30, restore_dir='restore_points'):
    """Factory function to get or create a backup manager instance"""
    return DatabaseBackupManager(db_path, backup_dir, max_backups, restore_dir)


def get_backup_scheduler(backup_manager, backup_time="02:00"):
    """Factory function to get backup scheduler"""
    return BackupScheduler(backup_manager, backup_time)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create backup manager
    bm = get_backup_manager()
    
    # Manual backup
    print("Creating manual backup...")
    bm.create_backup("manual_test")
    
    # List backups
    print("\nAvailable backups:")
    for backup in bm.get_backup_list():
        print(f"  - {backup['name']} ({backup['size']}) - {backup['created']}")
    
    # Start scheduler for automated backups
    print("\nStarting backup scheduler...")
    scheduler = get_backup_scheduler(bm, "02:00")
    scheduler.start()
    
    print("Backup system running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Stopped.")
