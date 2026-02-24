"""
Notification Service Module
Handles system notifications for the SMS application
"""

class NotificationService:
    """Service for managing notifications"""
    
    def __init__(self):
        self.notifications = []
    
    def send_notification(self, title, message, notification_type="info"):
        """
        Send a notification
        
        Args:
            title (str): Notification title
            message (str): Notification message
            notification_type (str): Type of notification (info, warning, error, success)
        """
        try:
            notification = {
                'title': title,
                'message': message,
                'type': notification_type
            }
            self.notifications.append(notification)
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def get_notifications(self):
        """Get all pending notifications"""
        return self.notifications
    
    def clear_notifications(self):
        """Clear all notifications"""
        self.notifications = []
    
    def log_event(self, event_type, description):
        """
        Log an event
        
        Args:
            event_type (str): Type of event
            description (str): Event description
        """
        try:
            # Store event for logging
            print(f"[{event_type}] {description}")
            return True
        except Exception as e:
            print(f"Error logging event: {e}")
            return False

# Create a singleton instance
_notification_service = None

def get_notification_service():
    """Get or create the notification service instance"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
