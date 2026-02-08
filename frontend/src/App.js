import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-brand">
            <h1>ChurnGuard AI</h1>
            <p>E-commerce Retention Platform</p>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/customers">Customers</Link></li>
            <li><Link to="/campaigns">Campaigns</Link></li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/campaigns" element={<div className="coming-soon">Campaigns page coming soon...</div>} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 ChurnGuard AI - Powered by ML ensemble (XGBoost + Neural Networks)</p>
          <p>85%+ prediction accuracy | 5-15% retention lift | 4.5x ROI</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
