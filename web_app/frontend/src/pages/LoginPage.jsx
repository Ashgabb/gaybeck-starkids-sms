import { useState } from 'react';
import './LoginPage.css';

export default function LoginPage({ onLogin, loading }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Gaybeck Starkids SMS</h1>
        <p className="subtitle">School Management System</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="credentials-info">
          <p>Demo Credentials:</p>
          <p>Admin: admin / admin123</p>
          <p>Teacher: teacher1 / teacher123</p>
          <p>Student: student1 / student123</p>
        </div>
        <div className="download-button-container">
          <a
            className="download-desktop-button"
            href="https://github.com/gaybeck/gaybeck-starkids-sms/archive/refs/heads/main.zip"
            target="_blank"
            rel="noopener noreferrer"
          >
            Download Desktop Version
          </a>
        </div>
      </div>
    </div>
  );
}
