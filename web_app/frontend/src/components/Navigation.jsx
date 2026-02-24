export default function Navigation({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>Gaybeck SMS</h1>
      </div>
      <div className="nav-user">
        <span>Welcome, {user.username}</span>
        <button onClick={onLogout}>Logout</button>
      </div>
    </nav>
  );
}
