"""
Biometric Authentication UI Components
Provides user interface for facial recognition and fingerprint integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from biometric_auth import BiometricAttendanceManager


class BiometricAttendanceUI:
    """UI for biometric-based attendance marking"""
    
    def __init__(self, parent, db_connection, person_id, person_type='student', callback=None):
        self.parent = parent
        self.conn = db_connection
        self.person_id = person_id
        self.person_type = person_type
        self.callback = callback
        self.manager = BiometricAttendanceManager(db_connection)
        self.is_processing = False
        
        self.create_ui()
    
    def create_ui(self):
        """Create biometric attendance UI"""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Biometric Attendance", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Choose biometric method to mark attendance",
                                font=('Segoe UI', 10))
        instructions.pack(pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Facial Recognition Button
        facial_btn = tk.Button(button_frame, text="📸\nFacial Recognition", 
                              command=self.start_facial_recognition,
                              width=20, height=8, bg='#3498db', fg='white',
                              font=('Segoe UI', 10, 'bold'))
        facial_btn.pack(side=tk.LEFT, padx=10)
        
        # Fingerprint Button
        fingerprint_btn = tk.Button(button_frame, text="👆\nFingerprint Sensor", 
                                   command=self.start_fingerprint_verification,
                                   width=20, height=8, bg='#27ae60', fg='white',
                                   font=('Segoe UI', 10, 'bold'))
        fingerprint_btn.pack(side=tk.LEFT, padx=10)
        
        # Status frame
        self.status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        self.status_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.status_text = tk.Text(self.status_frame, height=8, width=60, 
                                  bg='white', state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
    
    def start_facial_recognition(self):
        """Start facial recognition in thread"""
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing in progress")
            return
        
        self.is_processing = True
        thread = threading.Thread(target=self._do_facial_recognition)
        thread.start()
    
    def start_fingerprint_verification(self):
        """Start fingerprint verification in thread"""
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing in progress")
            return
        
        self.is_processing = True
        thread = threading.Thread(target=self._do_fingerprint_verification)
        thread.start()
    
    def _do_facial_recognition(self):
        """Perform facial recognition"""
        try:
            self.update_status("🔄 Starting facial recognition...")
            self.progress.start()
            
            success, message = self.manager.mark_attendance_with_facial(
                self.person_id, self.person_type
            )
            
            self.progress.stop()
            
            if success:
                self.update_status(f"✅ {message}\n\nAttendance marked successfully!")
                messagebox.showinfo("Success", message)
                if self.callback:
                    self.callback(True)
            else:
                self.update_status(f"❌ {message}\n\nPlease try again")
                messagebox.showerror("Failed", message)
        
        except Exception as e:
            self.progress.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.is_processing = False
    
    def _do_fingerprint_verification(self):
        """Perform fingerprint verification"""
        try:
            self.update_status("🔄 Waiting for fingerprint...")
            self.progress.start()
            
            success, message = self.manager.mark_attendance_with_fingerprint(
                self.person_id, self.person_type
            )
            
            self.progress.stop()
            
            if success:
                self.update_status(f"✅ {message}\n\nAttendance marked successfully!")
                messagebox.showinfo("Success", message)
                if self.callback:
                    self.callback(True)
            else:
                self.update_status(f"❌ {message}\n\nPlease try again")
                messagebox.showerror("Failed", message)
        
        except Exception as e:
            self.progress.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.is_processing = False
    
    def update_status(self, message):
        """Update status display"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete('1.0', tk.END)
        self.status_text.insert(tk.END, message)
        self.status_text.config(state=tk.DISABLED)


class BiometricEnrollmentUI:
    """UI for enrolling biometric data"""
    
    def __init__(self, parent, db_connection, person_id, person_name, person_type='student'):
        self.parent = parent
        self.conn = db_connection
        self.person_id = person_id
        self.person_name = person_name
        self.person_type = person_type
        self.manager = BiometricAttendanceManager(db_connection)
        self.is_enrolling = False
        
        self.create_ui()
    
    def create_ui(self):
        """Create enrollment UI"""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📝 Biometric Enrollment", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Info
        info = ttk.Label(main_frame, text=f"Enrolling: {self.person_name}",
                        font=('Segoe UI', 11))
        info.pack(pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Select Biometric Method", padding="10")
        options_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Facial Recognition Enrollment
        facial_frame = ttk.Frame(options_frame)
        facial_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(facial_frame, text="📸 Facial Recognition", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        ttk.Label(facial_frame, text="Capture 5 facial samples for recognition",
                 font=('Segoe UI', 9)).pack(anchor='w')
        
        ttk.Button(facial_frame, text="Enroll Facial Data", 
                  command=self.enroll_facial).pack(anchor='w', pady=5)
        
        # Fingerprint Enrollment
        fingerprint_frame = ttk.Frame(options_frame)
        fingerprint_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(fingerprint_frame, text="👆 Fingerprint Sensor", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        ttk.Label(fingerprint_frame, text="Enroll fingerprint for fast attendance marking",
                 font=('Segoe UI', 9)).pack(anchor='w')
        
        ttk.Button(fingerprint_frame, text="Enroll Fingerprint", 
                  command=self.enroll_fingerprint).pack(anchor='w', pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     font=('Segoe UI', 10), foreground='green')
        self.status_label.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X)
    
    def enroll_facial(self):
        """Enroll facial data"""
        if self.is_enrolling:
            messagebox.showwarning("Warning", "Enrollment in progress")
            return
        
        self.is_enrolling = True
        thread = threading.Thread(target=self._do_facial_enrollment)
        thread.start()
    
    def enroll_fingerprint(self):
        """Enroll fingerprint"""
        if self.is_enrolling:
            messagebox.showwarning("Warning", "Enrollment in progress")
            return
        
        self.is_enrolling = True
        thread = threading.Thread(target=self._do_fingerprint_enrollment)
        thread.start()
    
    def _do_facial_enrollment(self):
        """Perform facial enrollment"""
        try:
            self.update_status("🔄 Starting facial capture...")
            self.progress.start()
            
            success, message = self.manager.facial_system.capture_face_samples(
                self.person_id, self.person_name, num_samples=5
            )
            
            if success:
                self.update_status("🔄 Training facial recognition model...")
                train_success, train_msg = self.manager.facial_system.train_facial_recognition()
                
                self.progress.stop()
                
                if train_success:
                    self.update_status(f"✅ Facial enrollment complete!\n{train_msg}")
                    messagebox.showinfo("Success", "Facial data enrolled successfully!")
                else:
                    self.update_status(f"⚠️ {train_msg}")
                    messagebox.showwarning("Warning", train_msg)
            else:
                self.progress.stop()
                self.update_status(f"❌ {message}")
                messagebox.showerror("Failed", message)
        
        except Exception as e:
            self.progress.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.is_enrolling = False
    
    def _do_fingerprint_enrollment(self):
        """Perform fingerprint enrollment"""
        try:
            self.update_status("🔄 Enrolling fingerprint...")
            self.progress.start()
            
            success, message = self.manager.fingerprint_system.enroll_fingerprint(
                self.person_id, self.person_name
            )
            
            self.progress.stop()
            
            if success:
                self.update_status(f"✅ Fingerprint enrolled!\n{message}")
                messagebox.showinfo("Success", "Fingerprint enrolled successfully!")
            else:
                self.update_status(f"❌ {message}")
                messagebox.showerror("Failed", message)
        
        except Exception as e:
            self.progress.stop()
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.is_enrolling = False
    
    def update_status(self, message):
        """Update status display"""
        self.status_label.config(text=message, foreground='blue' if '🔄' in message else 
                                ('green' if '✅' in message else 'red'))
