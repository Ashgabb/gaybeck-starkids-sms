import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';
import TeacherDashboard from './pages/TeacherDashboard';
import StudentDashboard from './pages/StudentDashboard';
import Navigation from './components/Navigation';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (username, password) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        username,
        password
      });
      
      setUser(response.data.user);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  // Restore user from localStorage on mount
  if (!user && localStorage.getItem('user')) {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    setUser(storedUser);
  }

  if (!user) {
    return <LoginPage onLogin={handleLogin} loading={loading} />;
  }

  return (
    <Router>
      <div className="app">
        <Navigation user={user} onLogout={handleLogout} />
        <Routes>
          {user.role === 'admin' && (
            <Route path="/" element={<AdminDashboard />} />
          )}
          {user.role === 'teacher' && (
            <Route path="/" element={<TeacherDashboard />} />
          )}
          {user.role === 'student' && (
            <Route path="/" element={<StudentDashboard />} />
          )}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
