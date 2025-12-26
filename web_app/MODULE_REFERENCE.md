# Django Web App - Complete Module Reference

## 📊 All Django Apps & Models

### 1. Accounts App (Authentication & Users)
**Purpose**: User management and authentication

**Models:**
- `User` - Custom user model with email and roles
  - Fields: email, first_name, last_name, role, phone, profile_photo, is_active, created_at, updated_at
  - Methods: is_admin(), is_teacher(), is_accountant()

- `ActivityLog` - Activity tracking for auditing
  - Fields: user, action, model_name, object_id, details, ip_address, timestamp

**Views:**
- LoginView - User login
- LogoutView - User logout
- RegisterView - New user registration
- ProfileView - User profile viewing
- ProfileEditView - Edit user profile
- UserListView - List all users (Admin only)
- UserCreateView - Create new user (Admin only)
- UserEditView - Edit user (Admin only)
- UserDeleteView - Delete user (Admin only)

**URLs:**
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/register/`
- `/accounts/profile/`
- `/accounts/profile/edit/`
- `/accounts/users/`
- `/accounts/users/create/`
- `/accounts/users/<id>/edit/`
- `/accounts/users/<id>/delete/`

---

### 2. Students App (Student Management)
**Purpose**: Manage student information and documents

**Models:**
- `Student` - Student profile
  - Fields: name, registration_number, date_of_birth, gender, email, phone, address, class_name, guardian_name, guardian_phone, guardian_email, photo, is_active, admission_date

- `StudentDocument` - Document storage
  - Fields: student, document_type, file, uploaded_at

**Views:**
- StudentListView - List all students
- StudentCreateView - Add new student
- StudentDetailView - View student details
- StudentEditView - Edit student info
- StudentDeleteView - Delete student
- StudentDocumentListView - View student documents
- StudentDocumentCreateView - Upload document

**URLs:**
- `/students/`
- `/students/create/`
- `/students/<id>/`
- `/students/<id>/edit/`
- `/students/<id>/delete/`
- `/students/<id>/documents/`
- `/students/<id>/documents/add/`

---

### 3. Teachers App (Teacher Management)
**Purpose**: Manage teacher information and class assignments

**Models:**
- `Teacher` - Teacher profile
  - Fields: user (FK), employee_id, subject, qualifications, hire_date, is_active

- `ClassAssignment` - Teacher-class-subject assignments
  - Fields: teacher (FK), class_name, subject, semester, year, assigned_at

**Admin Interfaces:**
- TeacherAdmin - Manage teacher records
- ClassAssignmentAdmin - Manage class assignments

---

### 4. Attendance App (Attendance Tracking)
**Purpose**: Track student attendance daily

**Models:**
- `AttendanceRecord` - Daily attendance
  - Fields: student (FK), class_name, date, status (P/A/L/E), recorded_by (FK), notes
  - Status: Present, Absent, Late, Excused

**Views:**
- AttendanceListView - View all attendance records
- AttendanceByDateView - Filter by date
- ClassAttendanceView - View attendance by class
- StudentAttendanceView - View attendance by student
- AttendanceEditView - Edit attendance record

**URLs:**
- `/attendance/`
- `/attendance/date/<date>/`
- `/attendance/class/<class>/`
- `/attendance/student/<id>/`
- `/attendance/record/<id>/edit/`

---

### 5. Fees App (Fee Management)
**Purpose**: Manage student fees and payments

**Models:**
- `FeeType` - Fee categories
  - Fields: name, description, amount, is_active

- `StudentFee` - Fee assignments per student
  - Fields: student (FK), fee_type (FK), term, year, amount_due, amount_paid, due_date, is_paid
  - Methods: amount_pending (property)

- `FeePayment` - Payment records
  - Fields: student_fee (FK), amount, payment_method, payment_date, reference_number, notes, recorded_by
  - Payment methods: Cash, Check, Bank Transfer, Mobile Money, Other

**Views:**
- StudentFeeListView - List all fees
- StudentFeeDetailView - View fees for a student
- FeePaymentView - Record payment
- FeePaymentListView - View all payments

**URLs:**
- `/fees/`
- `/fees/student/<id>/`
- `/fees/<id>/pay/`
- `/fees/payments/`

---

### 6. Grading App (Grade Management)
**Purpose**: Record and track student grades

**Models:**
- `Grade` - Student grades per subject
  - Fields: student (FK), class_assignment (FK), term, year, mark (0-100), comments
  - Methods: grade_letter (property) - A/B/C/D/F
  - Terms: Term 1, Term 2, Term 3

**Views:**
- GradeListView - List all grades
- StudentGradeView - View grades by student
- GradeCreateView - Add new grade
- GradeEditView - Edit grade

**URLs:**
- `/grading/`
- `/grading/student/<id>/`
- `/grading/create/`
- `/grading/<id>/edit/`

---

### 7. Analytics App (Analytics & Reports)
**Purpose**: Provide AI-powered insights and analytics

**Models:**
- `AnalyticsReport` - Generated reports
  - Fields: report_type, title, description, data (JSON), generated_at

**Services:**
- `StudentAnalytics` - Student-level analytics
  - Methods:
    - get_attendance_risk() - Predict attendance risk
    - get_academic_performance() - Track grades
    - get_financial_status() - Monitor fees

- `ClassAnalytics` - Class-level analytics
  - Methods:
    - get_class_statistics() - Overall class metrics

**Views:**
- AnalyticsDashboardView - Main analytics dashboard
- StudentAnalyticsView - Student insights
- ClassAnalyticsView - Class insights
- AnalyticsReportsView - View all reports

**URLs:**
- `/analytics/dashboard/`
- `/analytics/student/<id>/`
- `/analytics/class/<class>/`
- `/analytics/reports/`

---

### 8. Dashboard App (Main Dashboard)
**Purpose**: Central overview and statistics

**Views:**
- DashboardView - Main dashboard with statistics
  - Statistics: Total students, teachers, pending fees, average grades
  - Recent: Students, attendance records

**URLs:**
- `/` or `/dashboard/`

---

## 🔗 Model Relationships

```
User (1) ──── (1) Teacher
    │
    └──── (N) ActivityLog

Student (1) ──── (N) AttendanceRecord
    │         ─── (N) Grade
    │         ─── (N) StudentFee
    │         ─── (N) StudentDocument

Teacher (1) ──── (N) ClassAssignment
    │
    └──── (N) AttendanceRecord (recorded_by)

ClassAssignment (1) ──── (N) Grade

FeeType (1) ──── (N) StudentFee

StudentFee (1) ──── (N) FeePayment
```

---

## 📋 URL Namespace Organization

| Namespace | Apps | URL Prefix |
|-----------|------|-----------|
| `accounts` | Accounts | `/accounts/` |
| `students` | Students | `/students/` |
| `teachers` | Teachers | `/teachers/` |
| `attendance` | Attendance | `/attendance/` |
| `fees` | Fees | `/fees/` |
| `grading` | Grading | `/grading/` |
| `analytics` | Analytics | `/analytics/` |
| `dashboard` | Dashboard | `/dashboard/` or `/` |

---

## 🔐 Permission & Access Control

### Admin Role
- ✅ Full access to all modules
- ✅ User management
- ✅ Activity log viewing
- ✅ Django admin access

### Teacher Role
- ✅ View assigned classes
- ✅ Record attendance
- ✅ Enter grades
- ✅ View student records

### Accountant Role
- ✅ Manage fees
- ✅ Record payments
- ✅ View fee reports
- ✅ Track financial status

---

## 📊 Form Classes

| App | Form Name | Purpose |
|-----|-----------|---------|
| accounts | CustomUserCreationForm | Create new user |
| accounts | CustomUserChangeForm | Edit user |
| accounts | LoginForm | User login |
| students | StudentForm | Add/edit student |
| students | StudentDocumentForm | Upload document |
| attendance | AttendanceForm | Record attendance |
| attendance | BulkAttendanceForm | Bulk attendance entry |
| fees | StudentFeeForm | Add fee |
| fees | FeePaymentForm | Record payment |
| grading | GradeForm | Add/edit grade |

---

## 📝 Admin Configurations

All apps have Django admin configurations:

- `accounts.admin.UserAdmin` - User management interface
- `accounts.admin.ActivityLogAdmin` - Activity log viewing
- `students.admin.StudentAdmin` - Student CRUD
- `students.admin.StudentDocumentAdmin` - Document management
- `teachers.admin.TeacherAdmin` - Teacher management
- `teachers.admin.ClassAssignmentAdmin` - Class assignments
- `attendance.admin.AttendanceRecordAdmin` - Attendance records
- `fees.admin.FeeTypeAdmin` - Fee type management
- `fees.admin.StudentFeeAdmin` - Student fees
- `fees.admin.FeePaymentAdmin` - Payment records
- `grading.admin.GradeAdmin` - Grade management
- `analytics.admin.AnalyticsReportAdmin` - Analytics reports

---

## 🎯 Template Structure

```
templates/
├── base.html                      # Main layout
├── accounts/
│   └── login.html
├── students/
│   ├── student_list.html
│   ├── student_form.html
│   ├── student_detail.html
│   ├── document_list.html
│   └── document_form.html
├── attendance/
│   ├── attendance_list.html
│   ├── attendance_by_date.html
│   ├── class_attendance.html
│   ├── student_attendance.html
│   └── attendance_form.html
├── fees/
│   ├── fee_list.html
│   ├── student_fee_detail.html
│   ├── payment_form.html
│   └── payment_list.html
├── grading/
│   ├── grade_list.html
│   ├── student_grades.html
│   └── grade_form.html
├── analytics/
│   ├── dashboard.html
│   ├── student_analytics.html
│   ├── class_analytics.html
│   └── reports_list.html
└── dashboard/
    └── home.html
```

---

## 🔧 Settings & Configuration

**Main Settings File**: `config/settings.py`

**Key Configurations:**
- Database: SQLite (development) or PostgreSQL (production)
- Authentication: Django session + custom user model
- Templates: Django templates with Bootstrap 5
- Static files: CSS, JavaScript, images
- Media files: Student photos, documents
- Installed apps: 8 custom + 6 Django
- Middleware: Security, CORS, CSRF protection
- Password validators: 4 validators

---

## 🚀 Ready for Production

All apps include:
- ✅ Proper error handling
- ✅ Form validation
- ✅ Authentication checks
- ✅ Permission verification
- ✅ Admin customization
- ✅ Model relationships
- ✅ Timestamps tracking
- ✅ Soft delete patterns
- ✅ Activity logging
- ✅ Comment documentation

---

**This completes your full Django web application!**

For more details, see:
- README.md - Full documentation
- QUICKSTART.md - Quick setup guide
- MIGRATION_GUIDE.md - Data migration help
