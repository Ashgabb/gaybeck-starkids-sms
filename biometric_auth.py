"""
Biometric Authentication Module for School Management System
Supports facial recognition and fingerprint sensor integration for attendance tracking
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import sqlite3
from datetime import datetime, date
import pickle
import os
from PIL import Image, ImageTk
import numpy as np
from threading import Thread, Lock
import time

try:
    from sklearn.preprocessing import LabelEncoder
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


class FacialRecognitionSystem:
    """Facial recognition for attendance using OpenCV"""
    
    # Standard face size for consistent recognition
    FACE_WIDTH = 100
    FACE_HEIGHT = 100
    
    def __init__(self, db_connection, data_dir="biometric_data"):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.data_dir = data_dir
        self.faces_dir = os.path.join(data_dir, "faces")
        self.models_dir = os.path.join(data_dir, "models")
        
        # Create directories if they don't exist
        os.makedirs(self.faces_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Initialize face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Initialize face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.model_path = os.path.join(self.models_dir, 'face_recognizer.yml')
        
        # Load trained model if exists
        if os.path.exists(self.model_path):
            try:
                self.recognizer.read(self.model_path)
            except:
                pass
        
        self.label_encoder = LabelEncoder() if ML_AVAILABLE else None
        self.lock = Lock()
    
    def capture_face_samples(self, person_id, person_name, num_samples=5, callback=None):
        """Capture facial samples for training"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return False, "Camera not available. Please check camera connection."
            
            # Set camera resolution for better performance
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            samples_captured = 0
            person_dir = os.path.join(self.faces_dir, str(person_id))
            os.makedirs(person_dir, exist_ok=True)
            
            # Clean old samples first
            for f in os.listdir(person_dir):
                try:
                    os.remove(os.path.join(person_dir, f))
                except:
                    pass
            
            frame_count = 0
            max_frames = 300  # Reduced timeout
            no_face_count = 0
            
            while samples_captured < num_samples and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Convert to grayscale and apply histogram equalization
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)  # Improve contrast for detection
                
                # Try multiple detection scales for better detection
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.2,  # Less aggressive scaling
                    minNeighbors=4,   # Reduced neighbors requirement
                    minSize=(30, 30)  # Smaller minimum size
                )
                
                if len(faces) > 0:
                    no_face_count = 0  # Reset no-face counter
                    # Take the largest face
                    (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
                    
                    samples_captured += 1
                    face_img = gray[y:y+h, x:x+w]
                    # Resize to standard size for consistent recognition
                    face_img = cv2.resize(face_img, (self.FACE_WIDTH, self.FACE_HEIGHT))
                    face_path = os.path.join(person_dir, f"sample_{samples_captured}.jpg")
                    cv2.imwrite(face_path, face_img)
                    
                    if callback:
                        callback(samples_captured, num_samples)
                else:
                    # No face detected
                    no_face_count += 1
                    # If no faces detected for too long, simplify detection further
                    if no_face_count > 50 and frame_count > 20:
                        # Try even more lenient detection
                        faces = self.face_cascade.detectMultiScale(
                            gray, 
                            scaleFactor=1.05,
                            minNeighbors=2,
                            minSize=(20, 20)
                        )
                        if len(faces) > 0:
                            no_face_count = 0
                            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
                            samples_captured += 1
                            face_img = gray[y:y+h, x:x+w]
                            face_img = cv2.resize(face_img, (self.FACE_WIDTH, self.FACE_HEIGHT))
                            face_path = os.path.join(person_dir, f"sample_{samples_captured}.jpg")
                            cv2.imwrite(face_path, face_img)
                            if callback:
                                callback(samples_captured, num_samples)
            
            cap.release()
            
            if samples_captured < 5:
                error_msg = f"Could only capture {samples_captured} facial samples. "
                if samples_captured == 0:
                    error_msg += "No faces detected. Please:\n"
                    error_msg += "1. Check camera is connected\n"
                    error_msg += "2. Ensure adequate lighting\n"
                    error_msg += "3. Position face directly at camera\n"
                    error_msg += "4. Keep face at 30-60cm distance"
                else:
                    error_msg += f"Need at least 5 samples to train."
                return False, error_msg
            
            return True, f"Successfully captured {samples_captured} facial samples"
        
        except Exception as e:
            try:
                cap.release()
            except:
                pass
            return False, f"Error capturing faces: {str(e)}"
    
    def train_facial_recognition(self):
        """Train facial recognition model"""
        try:
            faces = []
            labels = []
            label_map = {}
            current_label = 0
            
            # Load all face samples
            if not os.path.exists(self.faces_dir):
                return False, "No face samples directory found"
            
            for person_id in os.listdir(self.faces_dir):
                person_path = os.path.join(self.faces_dir, person_id)
                if not os.path.isdir(person_path):
                    continue
                
                label_map[current_label] = person_id
                person_samples = 0
                
                for img_file in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_file)
                    try:
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None and img.size > 0:
                            # Ensure consistent size
                            img = cv2.resize(img, (self.FACE_WIDTH, self.FACE_HEIGHT))
                            faces.append(img)
                            labels.append(current_label)
                            person_samples += 1
                    except:
                        continue
                
                if person_samples > 0:
                    current_label += 1
            
            if len(faces) < 5:
                return False, f"Insufficient face samples ({len(faces)} found). Need at least 5."
            
            # Train recognizer
            try:
                self.recognizer.train(faces, np.array(labels, dtype=np.int32))
                self.recognizer.write(self.model_path)
            except Exception as train_err:
                return False, f"Training failed: {str(train_err)}"
            
            # Save label mapping
            mapping_path = os.path.join(self.models_dir, 'label_map.pkl')
            with open(mapping_path, 'wb') as f:
                pickle.dump(label_map, f)
            
            return True, f"Successfully trained on {len(faces)} facial samples for {current_label} person(s)"
        
        except Exception as e:
            return False, f"Training error: {str(e)}"
    
    def recognize_face(self, confidence_threshold=50):
        """Recognize face from camera"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None, "Camera not available"
            
            # Set camera resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Load label map
            mapping_path = os.path.join(self.models_dir, 'label_map.pkl')
            label_map = {}
            if os.path.exists(mapping_path):
                try:
                    with open(mapping_path, 'rb') as f:
                        label_map = pickle.load(f)
                except:
                    pass
            
            if not label_map:
                return None, "No trained model found. Please enroll first."
            
            recognized_id = None
            max_frames = 300  # Timeout
            frame_count = 0
            
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)  # Improve contrast
                
                # Try detection with improved parameters
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.2,
                    minNeighbors=4,
                    minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    # Take the largest face
                    (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
                    face_img = gray[y:y+h, x:x+w]
                    # Resize to standard size for recognition
                    face_img = cv2.resize(face_img, (self.FACE_WIDTH, self.FACE_HEIGHT))
                    
                    # Recognize face
                    try:
                        label, confidence = self.recognizer.predict(face_img)
                        label = int(label)  # Ensure label is integer
                        
                        if confidence < confidence_threshold:
                            person_id = label_map.get(label, None)
                            if person_id:
                                recognized_id = str(person_id)
                                break  # Found a match, stop searching
                    except Exception as predict_error:
                        continue  # Skip this face if prediction fails
            
            cap.release()
            
            if recognized_id:
                return recognized_id, "Recognition successful"
            else:
                return None, "No matching face found"
        
        except Exception as e:
            try:
                cap.release()
            except:
                pass
            return None, f"Recognition error: {str(e)}"


class FingerprintSensorSimulator:
    """Fingerprint sensor simulator (can be replaced with actual hardware)"""
    
    def __init__(self, db_connection, data_dir="biometric_data"):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.data_dir = data_dir
        self.fingerprints_dir = os.path.join(data_dir, "fingerprints")
        os.makedirs(self.fingerprints_dir, exist_ok=True)
        self.lock = Lock()
    
    def enroll_fingerprint(self, person_id, person_name, callback=None):
        """Enroll fingerprint for a person"""
        try:
            # In a real system, this would interact with actual hardware
            # For now, we'll create a simulated fingerprint template
            
            person_dir = os.path.join(self.fingerprints_dir, str(person_id))
            os.makedirs(person_dir, exist_ok=True)
            
            # Simulate fingerprint capture (in real system, hardware would do this)
            fingerprint_template = {
                'person_id': person_id,
                'name': person_name,
                'enrollment_date': datetime.now().isoformat(),
                'template_data': np.random.randint(0, 255, 512).tobytes(),  # Simulated template
                'quality': 95
            }
            
            template_path = os.path.join(person_dir, 'fingerprint_template.pkl')
            with open(template_path, 'wb') as f:
                pickle.dump(fingerprint_template, f)
            
            # Also store in database for quick lookup
            self.cursor.execute("""
                INSERT OR REPLACE INTO biometric_fingerprints 
                (person_id, person_type, enrollment_date, quality_score)
                VALUES (?, ?, ?, ?)
            """, (person_id, 'student', datetime.now().isoformat(), 95))
            self.conn.commit()
            
            return True, "Fingerprint enrolled successfully"
        
        except Exception as e:
            return False, f"Enrollment error: {str(e)}"
    
    def verify_fingerprint(self, timeout=10):
        """Verify fingerprint and return person ID"""
        try:
            # Simulate fingerprint verification
            person_dir = self.fingerprints_dir
            
            # In a real system, hardware would capture and match
            # For simulation, we'll check available fingerprints
            recognized_id = None
            best_match = 0
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Simulate scanning (in real system, hardware does this)
                for person_id in os.listdir(person_dir):
                    person_path = os.path.join(person_dir, person_id)
                    if not os.path.isdir(person_path):
                        continue
                    
                    template_path = os.path.join(person_path, 'fingerprint_template.pkl')
                    if os.path.exists(template_path):
                        with open(template_path, 'rb') as f:
                            template = pickle.load(f)
                        
                        # Simulate matching score
                        match_score = np.random.randint(70, 100)
                        
                        if match_score > best_match and match_score > 80:
                            best_match = match_score
                            recognized_id = person_id
                
                if recognized_id:
                    break
                
                time.sleep(0.5)
            
            if recognized_id:
                return recognized_id, f"Fingerprint verified (Match: {best_match}%)"
            else:
                return None, "Fingerprint not recognized"
        
        except Exception as e:
            return None, f"Verification error: {str(e)}"


class BiometricAttendanceManager:
    """Manages biometric attendance for both students and staff"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.facial_system = FacialRecognitionSystem(db_connection)
        self.fingerprint_system = FingerprintSensorSimulator(db_connection)
        
        # Create biometric tables if they don't exist
        self._create_biometric_tables()
    
    def _create_biometric_tables(self):
        """Create necessary database tables"""
        try:
            # Facial recognition records
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS biometric_facial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    person_type TEXT,  -- 'student' or 'staff'
                    enrollment_date DATE,
                    samples_count INTEGER DEFAULT 0,
                    is_trained INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fingerprint records
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS biometric_fingerprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    person_type TEXT,  -- 'student' or 'staff'
                    enrollment_date DATE,
                    quality_score INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Biometric attendance logs
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS biometric_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    person_type TEXT,
                    biometric_method TEXT,  -- 'facial' or 'fingerprint'
                    recognition_confidence REAL,
                    attendance_date DATE,
                    attendance_time TIMESTAMP,
                    status TEXT,  -- 'verified' or 'failed'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(person_id, person_type, attendance_date)
                )
            ''')
            
            self.conn.commit()
        except Exception as e:
            print(f"Error creating biometric tables: {e}")
    
    def mark_attendance_with_facial(self, person_id, person_type='student'):
        """Mark attendance using facial recognition"""
        try:
            recognized_id, message = self.facial_system.recognize_face()
            
            if recognized_id and int(recognized_id) == person_id:
                # Check if attendance already marked today
                self.cursor.execute("""
                    SELECT id FROM biometric_attendance 
                    WHERE person_id=? AND person_type=? AND attendance_date=?
                """, (person_id, person_type, date.today()))
                
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing record
                    self.cursor.execute("""
                        UPDATE biometric_attendance 
                        SET biometric_method=?, recognition_confidence=?, 
                            attendance_time=?, status=?
                        WHERE person_id=? AND person_type=? AND attendance_date=?
                    """, ('facial', 90, datetime.now(), 'verified',
                          person_id, person_type, date.today()))
                else:
                    # Insert new record
                    self.cursor.execute("""
                        INSERT INTO biometric_attendance 
                        (person_id, person_type, biometric_method, recognition_confidence, 
                         attendance_date, attendance_time, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (person_id, person_type, 'facial', 90, date.today(), 
                          datetime.now(), 'verified'))
                
                self.conn.commit()
                status = "updated" if existing else "marked"
                return True, f"Attendance {status}: {message}"
            else:
                # Check if attendance already marked today
                self.cursor.execute("""
                    SELECT id FROM biometric_attendance 
                    WHERE person_id=? AND person_type=? AND attendance_date=?
                """, (person_id, person_type, date.today()))
                
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing record
                    self.cursor.execute("""
                        UPDATE biometric_attendance 
                        SET biometric_method=?, attendance_time=?, status=?
                        WHERE person_id=? AND person_type=? AND attendance_date=?
                    """, ('facial', datetime.now(), 'failed',
                          person_id, person_type, date.today()))
                else:
                    # Insert new record
                    self.cursor.execute("""
                        INSERT INTO biometric_attendance 
                        (person_id, person_type, biometric_method, attendance_date, 
                         attendance_time, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (person_id, person_type, 'facial', date.today(), 
                          datetime.now(), 'failed'))
                
                self.conn.commit()
                return False, "Facial recognition failed"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def mark_attendance_with_fingerprint(self, person_id, person_type='student'):
        """Mark attendance using fingerprint"""
        try:
            recognized_id, message = self.fingerprint_system.verify_fingerprint()
            
            if recognized_id and int(recognized_id) == person_id:
                # Check if attendance already marked today
                self.cursor.execute("""
                    SELECT id FROM biometric_attendance 
                    WHERE person_id=? AND person_type=? AND attendance_date=?
                """, (person_id, person_type, date.today()))
                
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing record
                    self.cursor.execute("""
                        UPDATE biometric_attendance 
                        SET biometric_method=?, recognition_confidence=?, 
                            attendance_time=?, status=?
                        WHERE person_id=? AND person_type=? AND attendance_date=?
                    """, ('fingerprint', 85, datetime.now(), 'verified',
                          person_id, person_type, date.today()))
                else:
                    # Insert new record
                    self.cursor.execute("""
                        INSERT INTO biometric_attendance 
                        (person_id, person_type, biometric_method, recognition_confidence, 
                         attendance_date, attendance_time, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (person_id, person_type, 'fingerprint', 85, date.today(), 
                          datetime.now(), 'verified'))
                
                self.conn.commit()
                status = "updated" if existing else "marked"
                return True, f"Attendance {status}: {message}"
            else:
                # Check if attendance already marked today
                self.cursor.execute("""
                    SELECT id FROM biometric_attendance 
                    WHERE person_id=? AND person_type=? AND attendance_date=?
                """, (person_id, person_type, date.today()))
                
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing record
                    self.cursor.execute("""
                        UPDATE biometric_attendance 
                        SET biometric_method=?, attendance_time=?, status=?
                        WHERE person_id=? AND person_type=? AND attendance_date=?
                    """, ('fingerprint', datetime.now(), 'failed',
                          person_id, person_type, date.today()))
                else:
                    # Insert new record
                    self.cursor.execute("""
                        INSERT INTO biometric_attendance 
                        (person_id, person_type, biometric_method, attendance_date, 
                         attendance_time, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (person_id, person_type, 'fingerprint', date.today(), 
                          datetime.now(), 'failed'))
                
                self.conn.commit()
                return False, "Fingerprint verification failed"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_biometric_stats(self, person_type='student'):
        """Get biometric enrollment statistics"""
        try:
            stats = {}
            
            # Facial recognition stats
            self.cursor.execute("""
                SELECT COUNT(*) as facial_enrolled
                FROM biometric_facial
                WHERE person_type = ? AND is_trained = 1
            """, (person_type,))
            stats['facial_enrolled'] = self.cursor.fetchone()[0] or 0
            
            # Fingerprint stats
            self.cursor.execute("""
                SELECT COUNT(*) as fingerprint_enrolled
                FROM biometric_fingerprints
                WHERE person_type = ?
            """, (person_type,))
            stats['fingerprint_enrolled'] = self.cursor.fetchone()[0] or 0
            
            # Biometric attendance today
            self.cursor.execute("""
                SELECT COUNT(*) as biometric_attendance_today
                FROM biometric_attendance
                WHERE person_type = ? AND attendance_date = ? AND status = 'verified'
            """, (person_type, date.today()))
            stats['biometric_attendance_today'] = self.cursor.fetchone()[0] or 0
            
            return stats
        
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
