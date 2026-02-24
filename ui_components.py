"""
UI Components Module
Provides custom UI components for the SMS application
"""
import tkinter as tk
from tkinter import ttk, messagebox

class NotificationCenterFrame(ttk.Frame):
    """Frame for notification center"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.notifications = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="Notification Center", font=("Arial", 12, "bold"))
        header.pack(pady=10)
        
        # Notification list
        self.notification_listbox = tk.Listbox(self, height=10)
        self.notification_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Mark as Read", command=self.mark_read).pack(side="left", padx=5)
    
    def add_notification(self, title, message):
        """Add a notification"""
        try:
            notification = f"{title}: {message}"
            self.notifications.append(notification)
            self.refresh_display()
            return True
        except Exception as e:
            print(f"Error adding notification: {e}")
            return False
    
    def refresh_display(self):
        """Refresh notification display"""
        try:
            self.notification_listbox.delete(0, tk.END)
            for notif in self.notifications:
                self.notification_listbox.insert(tk.END, notif)
        except Exception as e:
            print(f"Error refreshing display: {e}")
    
    def clear_all(self):
        """Clear all notifications"""
        self.notifications = []
        self.refresh_display()
    
    def mark_read(self):
        """Mark selected notification as read"""
        try:
            selection = self.notification_listbox.curselection()
            if selection:
                index = selection[0]
                self.notifications.pop(index)
                self.refresh_display()
        except Exception as e:
            print(f"Error marking as read: {e}")

class AITutorChatFrame(ttk.Frame):
    """Frame for AI tutor chat interface"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.chat_history = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="AI Tutor Chat", font=("Arial", 12, "bold"))
        header.pack(pady=10)
        
        # Chat display
        self.chat_text = tk.Text(self, height=15, state="disabled")
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Input area
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_text = ttk.Entry(input_frame)
        self.input_text.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side="left", padx=5)
    
    def send_message(self):
        """Send message to AI tutor"""
        try:
            message = self.input_text.get()
            if message.strip():
                self.chat_history.append(("You", message))
                self.chat_history.append(("AI Tutor", f"Response to: {message}"))
                self.input_text.delete(0, tk.END)
                self.refresh_display()
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def refresh_display(self):
        """Refresh chat display"""
        try:
            self.chat_text.config(state="normal")
            self.chat_text.delete("1.0", tk.END)
            for speaker, message in self.chat_history:
                self.chat_text.insert(tk.END, f"{speaker}: {message}\n\n")
            self.chat_text.config(state="disabled")
        except Exception as e:
            print(f"Error refreshing display: {e}")

class EWSDashboardFrame(ttk.Frame):
    """Frame for Early Warning System dashboard"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="Early Warning System Dashboard", font=("Arial", 12, "bold"))
        header.pack(pady=10)
        
        # Risk levels summary
        summary_frame = ttk.Frame(self)
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(summary_frame, text="High Risk: 5", foreground="red", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        ttk.Label(summary_frame, text="Medium Risk: 12", foreground="orange", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        ttk.Label(summary_frame, text="Low Risk: 83", foreground="green", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        
        # At-risk students list
        ttk.Label(self, text="At-Risk Students:").pack(anchor="w", padx=10, pady=(10, 0))
        
        self.students_listbox = tk.Listbox(self, height=10)
        self.students_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add sample data
        self.students_listbox.insert(tk.END, "Student 1 - High Risk (Attendance: 65%)")
        self.students_listbox.insert(tk.END, "Student 5 - Medium Risk (Grade: 58%)")
        self.students_listbox.insert(tk.END, "Student 12 - Medium Risk (Behavior Issues)")

class NotificationSettingsFrame(ttk.Frame):
    """Frame for notification settings"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="Notification Settings", font=("Arial", 12, "bold"))
        header.pack(pady=10)
        
        # Enable/disable notifications
        self.enable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Enable Notifications", variable=self.enable_var).pack(anchor="w", padx=10, pady=5)
        
        # Notification types
        ttk.Label(self, text="Notification Types:").pack(anchor="w", padx=10, pady=(10, 0))
        
        self.assessment_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Assessment Notifications", variable=self.assessment_var).pack(anchor="w", padx=20, pady=2)
        
        self.attendance_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Attendance Alerts", variable=self.attendance_var).pack(anchor="w", padx=20, pady=2)
        
        self.grade_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Grade Updates", variable=self.grade_var).pack(anchor="w", padx=20, pady=2)
        
        self.ews_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="EWS Alerts", variable=self.ews_var).pack(anchor="w", padx=20, pady=2)
        
        # Save button
        ttk.Button(self, text="Save Settings", command=self.save_settings).pack(pady=20)
    
    def save_settings(self):
        """Save notification settings"""
        messagebox.showinfo("Success", "Notification settings saved successfully!")
