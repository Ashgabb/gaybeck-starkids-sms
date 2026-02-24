"""
AI Learning UI Module
Provides GUI windows for AI-powered learning features
"""
import tkinter as tk
from tkinter import ttk, messagebox

class AITutorWindow(tk.Toplevel):
    """Window for AI tutoring interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Tutor")
        self.geometry("600x400")
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        # Header
        header = ttk.Label(self, text="AI Tutoring Assistant", font=("Arial", 14, "bold"))
        header.pack(pady=10)
        
        # Subject selection
        ttk.Label(self, text="Select Subject:").pack(anchor="w", padx=10)
        subject_var = tk.StringVar()
        subjects = ["Mathematics", "English", "Science", "History", "Geography"]
        ttk.Combobox(self, textvariable=subject_var, values=subjects, state="readonly").pack(fill="x", padx=10)
        
        # Topic input
        ttk.Label(self, text="Enter Topic/Question:").pack(anchor="w", padx=10, pady=(10, 0))
        self.query_text = tk.Text(self, height=5, width=60)
        self.query_text.pack(fill="both", padx=10, pady=5)
        
        # Get Response button
        ttk.Button(self, text="Get Tutoring Response", command=self.get_response).pack(pady=10)
        
        # Response area
        ttk.Label(self, text="Response:").pack(anchor="w", padx=10)
        self.response_text = tk.Text(self, height=10, width=60, state="disabled")
        self.response_text.pack(fill="both", padx=10, pady=5)
    
    def get_response(self):
        """Get tutoring response"""
        try:
            query = self.query_text.get("1.0", tk.END)
            if not query.strip():
                messagebox.showwarning("Input Required", "Please enter a question or topic")
                return
            
            response = f"AI Response: {query}\n\nThis is a tutoring response providing explanation and guidance."
            
            self.response_text.config(state="normal")
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", response)
            self.response_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Error getting response: {e}")

class LessonPlannerWindow(tk.Toplevel):
    """Window for AI lesson planning"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Lesson Planner")
        self.geometry("600x400")
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="AI Lesson Planner", font=("Arial", 14, "bold"))
        header.pack(pady=10)
        
        ttk.Label(self, text="Subject:").pack(anchor="w", padx=10)
        ttk.Entry(self).pack(fill="x", padx=10)
        
        ttk.Label(self, text="Topic:").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Entry(self).pack(fill="x", padx=10)
        
        ttk.Label(self, text="Duration (minutes):").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Entry(self).pack(fill="x", padx=10)
        
        ttk.Button(self, text="Generate Lesson Plan").pack(pady=10)
        
        ttk.Label(self, text="Generated Plan:").pack(anchor="w", padx=10)
        self.plan_text = tk.Text(self, height=15, width=60)
        self.plan_text.pack(fill="both", padx=10, pady=5)

class QuizGeneratorWindow(tk.Toplevel):
    """Window for AI quiz generation"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Quiz Generator")
        self.geometry("600x400")
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="AI Quiz Generator", font=("Arial", 14, "bold"))
        header.pack(pady=10)
        
        ttk.Label(self, text="Topic:").pack(anchor="w", padx=10)
        ttk.Entry(self).pack(fill="x", padx=10)
        
        ttk.Label(self, text="Number of Questions:").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Spinbox(self, from_=1, to=50).pack(fill="x", padx=10)
        
        ttk.Label(self, text="Difficulty:").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Combobox(self, values=["Easy", "Medium", "Hard"], state="readonly").pack(fill="x", padx=10)
        
        ttk.Button(self, text="Generate Quiz").pack(pady=10)
        
        ttk.Label(self, text="Quiz Preview:").pack(anchor="w", padx=10)
        self.quiz_text = tk.Text(self, height=15, width=60)
        self.quiz_text.pack(fill="both", padx=10, pady=5)

class AssignmentGraderWindow(tk.Toplevel):
    """Window for AI assignment grading"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Assignment Grader")
        self.geometry("600x400")
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        header = ttk.Label(self, text="AI Assignment Grader", font=("Arial", 14, "bold"))
        header.pack(pady=10)
        
        ttk.Label(self, text="Assignment Type:").pack(anchor="w", padx=10)
        ttk.Combobox(self, values=["Essay", "Problem Set", "Project", "Writing"], state="readonly").pack(fill="x", padx=10)
        
        ttk.Label(self, text="Student Submission:").pack(anchor="w", padx=10, pady=(10, 0))
        self.submission_text = tk.Text(self, height=10, width=60)
        self.submission_text.pack(fill="both", padx=10, pady=5)
        
        ttk.Button(self, text="Grade Assignment").pack(pady=10)
        
        ttk.Label(self, text="Grade & Feedback:").pack(anchor="w", padx=10)
        self.feedback_text = tk.Text(self, height=8, width=60)
        self.feedback_text.pack(fill="both", padx=10, pady=5)
