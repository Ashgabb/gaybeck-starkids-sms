# Gaybeck Starkids SMS - Web App

Web-based wrapper for the Gaybeck Starkids School Management System.

## Structure

- `backend/` - Flask API server
- `frontend/` - React web interface

> The web app is independent from the desktop app. The desktop version now includes an "Open Web App" launcher, and the web app includes a download button for the desktop source package.

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000/api`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The web app will be available at `http://localhost:3000`

## Features

- User authentication (Admin, Teacher, Student)
- Dashboard views for all roles
- Student management
- Teacher management
- AI Assessment creation and management
- Admin settings and backups

## API Endpoints

- `POST /api/auth/login` - User login
- `GET /api/students` - Get all students
- `GET /api/teachers` - Get all teachers
- `GET /api/assessments` - Get all assessments
- `POST /api/assessments` - Create assessment
- `GET /api/admin/dashboard` - Admin dashboard data
