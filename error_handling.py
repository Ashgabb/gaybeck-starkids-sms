"""
Comprehensive Logging and Error Handling System
Provides centralized logging, error tracking, and performance metrics
Version: 1.0.0
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from functools import wraps
import time
import sqlite3

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

class LoggerSetup:
    """Configure logging for the application"""
    
    @staticmethod
    def setup_logging(log_level=logging.INFO, log_file='logs/sms_application.log'):
        """
        Setup comprehensive logging configuration
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger('SMS')
        logger.setLevel(log_level)

        # Avoid duplicate handlers when setup is called multiple times.
        if logger.handlers:
            return logger
        
        # Format: timestamp - logger - level - message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10  # Keep 10 backup files
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger


def log_errors(func):
    """
    Decorator to log function errors and execution time
    Usage: @log_errors
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('SMS')
        func_name = func.__name__
        start_time = time.time()
        
        try:
            logger.debug(f"Executing: {func_name} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"✅ {func_name} completed in {elapsed:.3f}s")
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ {func_name} failed after {elapsed:.3f}s: {str(e)}", exc_info=True)
            raise
    
    return wrapper


def log_performance(threshold_ms=1000):
    """
    Decorator to log performance warnings if execution exceeds threshold
    Usage: @log_performance(threshold_ms=500)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger('SMS')
            func_name = func.__name__
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                elapsed_ms = (time.time() - start_time) * 1000
                
                if elapsed_ms > threshold_ms:
                    logger.warning(f"⚠️ {func_name} slow execution: {elapsed_ms:.1f}ms")
                else:
                    logger.debug(f"{func_name} executed in {elapsed_ms:.1f}ms")
                
                return result
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                logger.error(f"❌ {func_name} failed after {elapsed_ms:.1f}ms: {str(e)}", exc_info=True)
                raise
        
        return wrapper
    return decorator


class DatabaseErrorHandler:
    """Handle database-related errors with logging and recovery"""
    
    @staticmethod
    def handle_db_error(operation_name, error, logger=None):
        """
        Handle database errors with context
        
        Args:
            operation_name: Name of the failed operation
            error: The exception
            logger: Logger instance
        """
        if logger is None:
            logger = logging.getLogger('SMS')
        
        error_msg = str(error)
        
        if 'database is locked' in error_msg.lower():
            logger.warning(f"Database locked during {operation_name}. Retrying...")
            return 'RETRY'
        
        elif 'no such table' in error_msg.lower():
            logger.error(f"Database schema error in {operation_name}: {error}")
            return 'SCHEMA_ERROR'
        
        elif 'constraint failed' in error_msg.lower():
            logger.error(f"Constraint violation in {operation_name}: {error}")
            return 'CONSTRAINT_ERROR'
        
        else:
            logger.error(f"Database error in {operation_name}: {error}", exc_info=True)
            return 'GENERAL_ERROR'
    
    @staticmethod
    def retry_db_operation(operation, max_retries=3, delay=0.5):
        """
        Retry a database operation with exponential backoff
        
        Args:
            operation: Callable that performs the DB operation
            max_retries: Maximum retry attempts
            delay: Initial delay between retries
            
        Returns:
            Result of the operation or None if all retries failed
        """
        logger = logging.getLogger('SMS')
        
        for attempt in range(max_retries):
            try:
                return operation()
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e) and attempt < max_retries - 1:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"DB locked, retry {attempt+1}/{max_retries} after {wait_time:.2f}s")
                    time.sleep(wait_time)
                else:
                    raise
        
        return None


class PerformanceMonitor:
    """Track and log performance metrics"""
    
    def __init__(self, db_path='school_management.db'):
        """
        Initialize performance monitor
        
        Args:
            db_path: Path to database for storing metrics
        """
        self.db_path = db_path
        self.logger = logging.getLogger('SMS')
        self._ensure_metrics_table()
    
    def _ensure_metrics_table(self):
        """Create performance_metrics table if it doesn't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'success'
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to create performance_metrics table: {e}")
    
    def log_operation(self, operation_name, duration_ms, status='success'):
        """Log an operation's performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics (operation, duration_ms, status)
                VALUES (?, ?, ?)
            ''', (operation_name, duration_ms, status))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to log performance metric: {e}")
    
    def get_operation_stats(self, operation_name, hours=24):
        """Get performance statistics for an operation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as count,
                    AVG(duration_ms) as avg_ms,
                    MIN(duration_ms) as min_ms,
                    MAX(duration_ms) as max_ms
                FROM performance_metrics
                WHERE operation = ? AND status = 'success'
                AND timestamp > datetime('now', '-' || ? || ' hours')
            ''', (operation_name, hours))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'count': result[0],
                    'avg_ms': result[1],
                    'min_ms': result[2],
                    'max_ms': result[3]
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve performance stats: {e}")
            return None


def setup_application_logging():
    """Initialize application-wide logging"""
    level_name = os.getenv('SMS_LOG_LEVEL', 'INFO').upper()
    resolved_level = getattr(logging, level_name, logging.INFO)
    logger = LoggerSetup.setup_logging(
        log_level=resolved_level,
        log_file='logs/sms_application.log'
    )
    
    logger.info("=" * 70)
    logger.info("SMS APPLICATION STARTED")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Python Version: {sys.version}")
    logger.info("=" * 70)
    
    return logger


if __name__ == "__main__":
    # Test the logging system
    logger = LoggerSetup.setup_logging(log_level=logging.DEBUG)
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Test performance monitor
    pm = PerformanceMonitor()
    pm.log_operation("test_operation", 125.5)
    stats = pm.get_operation_stats("test_operation")
    print(f"\nPerformance Stats: {stats}")
