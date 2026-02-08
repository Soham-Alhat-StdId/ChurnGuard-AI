import React, { useState, useEffect } from 'react';
import { getCustomers, predictChurn } from '../services/api';
import './Customers.css';

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await getCustomers(0, 100);
      setCustomers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load customers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePredictChurn = async (customerId) => {
    try {
      const response = await predictChurn(customerId);
      setPrediction(response.data);
      setSelectedCustomer(customerId);
    } catch (err) {
      console.error('Prediction failed:', err);
      alert('Failed to predict churn for this customer');
    }
  };

  if (loading) return <div className="loading">Loading customers...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="customers-page">
      <h1>Customer Management</h1>
      
      <div className="customers-grid">
        <div className="customers-list">
          <h2>All Customers ({customers.length})</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Orders</th>
                  <th>Total Spent</th>
                  <th>Risk Level</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {customers.map(customer => (
                  <tr 
                    key={customer.id}
                    className={selectedCustomer === customer.id ? 'selected' : ''}
                  >
                    <td>{customer.id}</td>
                    <td>{customer.name}</td>
                    <td>{customer.email}</td>
                    <td>{customer.total_orders}</td>
                    <td>${customer.total_spent.toFixed(2)}</td>
                    <td>
                      {customer.churn_risk_level ? (
                        <span className={`risk-badge ${customer.churn_risk_level}`}>
                          {customer.churn_risk_level}
                        </span>
                      ) : (
                        <span className="risk-badge">N/A</span>
                      )}
                    </td>
                    <td>
                      <button 
                        className="btn-predict"
                        onClick={() => handlePredictChurn(customer.id)}
                      >
                        Predict
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {prediction && selectedCustomer && (
          <div className="prediction-panel">
            <h2>Prediction Results</h2>
            <div className="prediction-content">
              <div className="prediction-score">
                <h3>Ensemble Score</h3>
                <div className={`score-circle ${prediction.risk_level}`}>
                  {(prediction.ensemble_score * 100).toFixed(1)}%
                </div>
                <p className="risk-label">Risk Level: <strong>{prediction.risk_level}</strong></p>
              </div>

              <div className="model-scores">
                <div className="model-score">
                  <h4>XGBoost Model</h4>
                  <p>{(prediction.xgboost_score * 100).toFixed(1)}%</p>
                </div>
                <div className="model-score">
                  <h4>Neural Network</h4>
                  <p>{(prediction.nn_score * 100).toFixed(1)}%</p>
                </div>
              </div>

              <div className="shap-explanation">
                <h3>Top Contributing Factors (SHAP)</h3>
                <ul>
                  {prediction.top_features.map((feature, idx) => (
                    <li key={idx}>
                      <span className="feature-name">{feature.feature}</span>
                      <span className="feature-value">
                        Impact: {feature.shap_value.toFixed(3)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Customers;
