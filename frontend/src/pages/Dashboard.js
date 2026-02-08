import React, { useState, useEffect } from 'react';
import { getDashboardMetrics, getHighRiskCustomers } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [highRiskCustomers, setHighRiskCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [metricsResponse, customersResponse] = await Promise.all([
        getDashboardMetrics(),
        getHighRiskCustomers(10)
      ]);
      
      setMetrics(metricsResponse.data);
      setHighRiskCustomers(customersResponse.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!metrics) return <div>No data available</div>;

  return (
    <div className="dashboard">
      <h1>ChurnGuard AI Dashboard</h1>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Customers</h3>
          <p className="metric-value">{metrics.total_customers}</p>
        </div>
        
        <div className="metric-card high-risk">
          <h3>High Risk</h3>
          <p className="metric-value">{metrics.high_risk_customers}</p>
        </div>
        
        <div className="metric-card medium-risk">
          <h3>Medium Risk</h3>
          <p className="metric-value">{metrics.medium_risk_customers}</p>
        </div>
        
        <div className="metric-card low-risk">
          <h3>Low Risk</h3>
          <p className="metric-value">{metrics.low_risk_customers}</p>
        </div>
        
        <div className="metric-card">
          <h3>Avg Churn Probability</h3>
          <p className="metric-value">
            {(metrics.avg_churn_probability * 100).toFixed(1)}%
          </p>
        </div>
        
        <div className="metric-card">
          <h3>Avg Customer Lifetime Value</h3>
          <p className="metric-value">
            ${metrics.avg_clv.toFixed(2)}
          </p>
        </div>
        
        <div className="metric-card">
          <h3>Retention Lift</h3>
          <p className="metric-value">{metrics.retention_lift}%</p>
        </div>
        
        <div className="metric-card">
          <h3>ROI</h3>
          <p className="metric-value">{metrics.roi}x</p>
        </div>
      </div>

      <div className="high-risk-section">
        <h2>High Risk Customers (Top 10)</h2>
        <div className="customer-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Churn Probability</th>
                <th>Risk Level</th>
                <th>Total Spent</th>
                <th>Last Order</th>
              </tr>
            </thead>
            <tbody>
              {highRiskCustomers.map(customer => (
                <tr key={customer.id}>
                  <td>{customer.id}</td>
                  <td>{customer.name}</td>
                  <td>{customer.email}</td>
                  <td>
                    <span className="probability">
                      {customer.churn_probability 
                        ? (customer.churn_probability * 100).toFixed(1) + '%'
                        : 'N/A'}
                    </span>
                  </td>
                  <td>
                    <span className={`risk-badge ${customer.churn_risk_level}`}>
                      {customer.churn_risk_level || 'N/A'}
                    </span>
                  </td>
                  <td>${customer.total_spent.toFixed(2)}</td>
                  <td>{customer.days_since_last_order} days ago</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="actions">
        <button 
          className="btn btn-primary"
          onClick={() => window.location.href = '/customers'}
        >
          View All Customers
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => window.location.href = '/campaigns'}
        >
          Manage Campaigns
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
