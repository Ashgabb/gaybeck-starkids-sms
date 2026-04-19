export default function Navigation({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>Gaybeck SMS</h1>
      </div>
      <div className="nav-user">
        <span>Welcome, {user.username}</span>
        <a
          className="download-desktop-button"
          href="https://github.com/gaybeck/gaybeck-starkids-sms/archive/refs/heads/main.zip"
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Desktop
        </a>
        <button onClick={onLogout}>Logout</button>
      </div>
    </nav>
  );
}
