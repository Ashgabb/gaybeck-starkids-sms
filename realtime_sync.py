#!/usr/bin/env python3
"""
Real-time Synchronization Interface for School Management System
==============================================================
This module provides real-time data synchronization, activity logging,
and dashboard updates for all user operations and system activities.
"""

import sqlite3
from datetime import datetime
import json
import threading
import time

class RealTimeSyncManager:
    """Manages real-time synchronization and activity logging"""
    
    def __init__(self, db_path='school_management.db'):
        self.db_path = db_path
        self.is_monitoring = False
        self.monitor_thread = None
        
    def log_user_activity(self, username, action_type, table_affected, record_id=None, 
                         old_values=None, new_values=None, details=None):
        """Log user activity for audit trail"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_activity_log (
                    username, action_type, table_affected, record_id,
                    old_values, new_values, details, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                username, action_type, table_affected, record_id,
                json.dumps(old_values) if old_values else None,
                json.dumps(new_values) if new_values else None,
                details
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
    
    def create_system_notification(self, title, message, notification_type='info', 
                                 user_id=None, action_url=None, priority=1):
        """Create a system notification"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO system_notifications (
                    user_id, title, message, notification_type, 
                    action_url, priority, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            """, (user_id, title, message, notification_type, action_url, priority))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error creating notification: {str(e)}")
    
    def update_statistics_cache(self, metric_name, metric_value, metric_data=None, category='general'):
        """Update cached statistics for performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO statistics_cache (
                    metric_name, metric_value, metric_data, category, calculated_at
                ) VALUES (?, ?, ?, ?, datetime('now'))
            """, (metric_name, metric_value, json.dumps(metric_data) if metric_data else None, category))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating statistics: {str(e)}")
    
    def get_real_time_dashboard_data(self):
        """Get real-time dashboard statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get dashboard stats from view
            cursor.execute("SELECT * FROM dashboard_stats")
            dashboard_data = {}
            
            for row in cursor.fetchall():
                metric, value, calculated_at = row
                dashboard_data[metric] = {
                    'value': value,
                    'calculated_at': calculated_at
                }
            
            # Get recent activities
            cursor.execute("SELECT * FROM recent_activities LIMIT 10")
            recent_activities = [
                {
                    'source': row[0],
                    'username': row[1], 
                    'activity': row[2],
                    'entity': row[3],
                    'timestamp': row[4],
                    'details': row[5]
                }
                for row in cursor.fetchall()
            ]
            
            # Get unread notifications
            cursor.execute("""
                SELECT id, title, message, notification_type, created_at, priority 
                FROM system_notifications 
                WHERE is_read = FALSE 
                ORDER BY priority DESC, created_at DESC 
                LIMIT 5
            """)
            notifications = [
                {
                    'id': row[0],
                    'title': row[1],
                    'message': row[2],
                    'type': row[3],
                    'created_at': row[4],
                    'priority': row[5]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            return {
                'dashboard_data': dashboard_data,
                'recent_activities': recent_activities,
                'notifications': notifications,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting dashboard data: {str(e)}")
            return {}
    
    def get_student_performance_data(self, student_id=None):
        """Get comprehensive student performance data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if student_id:
                cursor.execute("SELECT * FROM student_performance WHERE id = ?", (student_id,))
                data = cursor.fetchone()
                if data:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, data))
            else:
                cursor.execute("SELECT * FROM student_performance ORDER BY attendance_percentage DESC")
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in data]
            
            conn.close()
            
        except Exception as e:
            print(f"Error getting student performance data: {str(e)}")
            return []
    
    def get_financial_summary_data(self):
        """Get financial summary and analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM financial_summary")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            conn.close()
            return [dict(zip(columns, row)) for row in data]
            
        except Exception as e:
            print(f"Error getting financial summary: {str(e)}")
            return []
    
    def get_class_analytics_data(self):
        """Get class analytics and performance data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM class_analytics")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            conn.close()
            return [dict(zip(columns, row)) for row in data]
            
        except Exception as e:
            print(f"Error getting class analytics: {str(e)}")
            return []
    
    def mark_notification_as_read(self, notification_id):
        """Mark a notification as read"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE system_notifications 
                SET is_read = TRUE 
                WHERE id = ?
            """, (notification_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error marking notification as read: {str(e)}")
    
    def cleanup_old_data(self, days_to_keep=90):
        """Clean up old activity logs and notifications"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clean up old activity logs
            cursor.execute("""
                DELETE FROM user_activity_log 
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days_to_keep))
            logs_deleted = cursor.rowcount
            
            # Clean up old notifications
            cursor.execute("""
                DELETE FROM system_notifications 
                WHERE created_at < datetime('now', '-{} days') 
                AND is_read = TRUE
            """.format(days_to_keep))
            notifications_deleted = cursor.rowcount
            
            # Clean up expired statistics
            cursor.execute("""
                DELETE FROM statistics_cache 
                WHERE expires_at IS NOT NULL 
                AND expires_at < datetime('now')
            """)
            stats_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            return {
                'logs_deleted': logs_deleted,
                'notifications_deleted': notifications_deleted,
                'stats_deleted': stats_deleted
            }
            
        except Exception as e:
            print(f"Error cleaning up data: {str(e)}")
            return {}
    
    def refresh_all_statistics(self):
        """Refresh all cached statistics"""
        try:
            # Get fresh statistics
            dashboard_data = self.get_real_time_dashboard_data()
            
            # Update individual metrics
            for metric, data in dashboard_data.get('dashboard_data', {}).items():
                self.update_statistics_cache(metric, data['value'])
            
            # Calculate additional metrics
            self._calculate_performance_metrics()
            
            return True
            
        except Exception as e:
            print(f"Error refreshing statistics: {str(e)}")
            return False
    
    def _calculate_performance_metrics(self):
        """Calculate and cache performance metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate attendance trends
            cursor.execute("""
                SELECT date, 
                       COUNT(CASE WHEN present = 1 THEN 1 END) * 100.0 / COUNT(*) as rate
                FROM attendance 
                WHERE date >= date('now', '-7 days')
                GROUP BY date
                ORDER BY date
            """)
            
            attendance_trends = []
            for row in cursor.fetchall():
                attendance_trends.append({
                    'date': row[0],
                    'rate': round(row[1], 2)
                })
            
            self.update_statistics_cache(
                'attendance_trends_7days', 
                len(attendance_trends), 
                attendance_trends,
                'performance'
            )
            
            # Calculate fee collection rates
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN amount_paid >= tuition_fee + feeding_fee + bus_fee + other_fees THEN 1 END) * 100.0 / COUNT(*) as collection_rate
                FROM fees
            """)
            
            result = cursor.fetchone()
            collection_rate = round(result[0], 2) if result and result[0] else 0
            
            self.update_statistics_cache(
                'fee_collection_rate',
                collection_rate,
                category='financial'
            )
            
            # Calculate class capacity utilization
            cursor.execute("""
                SELECT c.class_name, c.capacity, COUNT(s.id) as enrolled,
                       COUNT(s.id) * 100.0 / c.capacity as utilization
                FROM classes c
                LEFT JOIN students s ON c.id = s.class_id
                GROUP BY c.id, c.class_name, c.capacity
            """)
            
            capacity_data = []
            for row in cursor.fetchall():
                capacity_data.append({
                    'class_name': row[0],
                    'capacity': row[1],
                    'enrolled': row[2],
                    'utilization': round(row[3], 2)
                })
            
            self.update_statistics_cache(
                'class_capacity_utilization',
                len(capacity_data),
                capacity_data,
                'academic'
            )
            
            conn.close()
            
        except Exception as e:
            print(f"Error calculating performance metrics: {str(e)}")
    
    def start_background_monitoring(self):
        """Start background monitoring for real-time updates"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._background_monitor)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
    
    def stop_background_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _background_monitor(self):
        """Background monitoring thread"""
        while self.is_monitoring:
            try:
                # Refresh statistics every 5 minutes
                self.refresh_all_statistics()
                
                # Clean up old data once per day (check every hour)
                current_hour = datetime.now().hour
                if current_hour == 2:  # 2 AM cleanup
                    self.cleanup_old_data()
                
                # Sleep for 5 minutes
                time.sleep(300)
                
            except Exception as e:
                print(f"Error in background monitoring: {str(e)}")
                time.sleep(60)  # Wait 1 minute on error

# Global sync manager instance
sync_manager = RealTimeSyncManager()

# Helper functions for easy integration
def log_activity(username, action, table, record_id=None, old_data=None, new_data=None, details=None):
    """Log user activity - easy integration function"""
    sync_manager.log_user_activity(username, action, table, record_id, old_data, new_data, details)

def notify_system(title, message, msg_type='info', user_id=None, url=None, priority=1):
    """Create system notification - easy integration function"""
    sync_manager.create_system_notification(title, message, msg_type, user_id, url, priority)

def update_metric(name, value, data=None, category='general'):
    """Update statistics metric - easy integration function"""
    sync_manager.update_statistics_cache(name, value, data, category)

def get_dashboard():
    """Get dashboard data - easy integration function"""
    return sync_manager.get_real_time_dashboard_data()

def get_student_stats(student_id=None):
    """Get student performance data - easy integration function"""
    return sync_manager.get_student_performance_data(student_id)

def get_financial_stats():
    """Get financial summary - easy integration function"""
    return sync_manager.get_financial_summary_data()

def get_class_stats():
    """Get class analytics - easy integration function"""
    return sync_manager.get_class_analytics_data()

def start_monitoring():
    """Start background monitoring - easy integration function"""
    sync_manager.start_background_monitoring()

def stop_monitoring():
    """Stop background monitoring - easy integration function"""
    sync_manager.stop_background_monitoring()

if __name__ == "__main__":
    # Demo usage
    print("🔄 Real-time Synchronization Manager Demo")
    print("=" * 50)
    
    # Test logging
    log_activity('admin', 'TEST', 'demo_table', 1, {'old': 'value'}, {'new': 'value'}, 'Demo activity')
    print("✅ Activity logged successfully")
    
    # Test notification
    notify_system('Test Notification', 'This is a test notification from the sync system', 'info')
    print("✅ Notification created successfully")
    
    # Test dashboard data
    dashboard = get_dashboard()
    print(f"✅ Dashboard data retrieved: {len(dashboard.get('dashboard_data', {}))} metrics")
    
    # Test statistics update
    update_metric('demo_metric', 42, {'extra': 'data'}, 'demo')
    print("✅ Metric updated successfully")
    
    print("\n🎯 Real-time synchronization system is ready for integration!")