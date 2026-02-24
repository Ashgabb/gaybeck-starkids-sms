export default function AdminDashboard() {
  return (
    <div className="dashboard">
      <h2>Admin Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>150</h3>
          <p>Total Students</p>
        </div>
        <div className="stat-card">
          <h3>35</h3>
          <p>Total Teachers</p>
        </div>
        <div className="stat-card">
          <h3>42</h3>
          <p>Active Assessments</p>
        </div>
        <div className="stat-card">
          <h3>12</h3>
          <p>Active Sessions</p>
        </div>
      </div>
    </div>
  );
}
