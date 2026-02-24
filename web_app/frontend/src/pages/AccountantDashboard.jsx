import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';

function AccountantDashboard() {
  const [transactions, setTransactions] = useState([]);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/financial-transactions', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTransactions(data.transactions || []);
        setReport(data.summary || null);
      }
    } catch (err) {
      console.error('Error fetching transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Accountant Dashboard</h1>
      
      {report && (
        <div className="summary-cards">
          <div className="card">
            <h3>Total Fees Collected</h3>
            <p className="amount">${report.total_collected}</p>
          </div>
          <div className="card">
            <h3>Outstanding Fees</h3>
            <p className="amount">${report.total_outstanding}</p>
          </div>
          <div className="card">
            <h3>Pending Payments</h3>
            <p className="amount">${report.total_pending}</p>
          </div>
        </div>
      )}
      
      <div className="transactions-section">
        <h2>Recent Transactions</h2>
        <table className="transactions-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Student</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id}>
                <td>{t.date}</td>
                <td>{t.student_name}</td>
                <td>${t.amount}</td>
                <td>{t.status}</td>
                <td>{t.type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AccountantDashboard;
