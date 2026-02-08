import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Customers
export const getCustomers = (skip = 0, limit = 100) => 
  api.get(`/customers?skip=${skip}&limit=${limit}`);

export const getCustomer = (customerId) => 
  api.get(`/customers/${customerId}`);

export const createCustomer = (customerData) => 
  api.post('/customers', customerData);

export const updateCustomer = (customerId, customerData) => 
  api.put(`/customers/${customerId}`, customerData);

export const deleteCustomer = (customerId) => 
  api.delete(`/customers/${customerId}`);

// Predictions
export const predictChurn = (customerId) => 
  api.post('/predictions/predict', { customer_id: customerId });

export const predictChurnBatch = (customerIds) => 
  api.post('/predictions/predict/batch', customerIds);

export const getHighRiskCustomers = (limit = 100) => 
  api.get(`/predictions/high-risk?limit=${limit}`);

export const predictCLV = (customerId) => 
  api.post('/predictions/clv/predict', { customer_id: customerId });

export const detectAnomalies = (customerId) => 
  api.post(`/predictions/anomaly/detect?customer_id=${customerId}`);

// Campaigns
export const getCampaigns = (skip = 0, limit = 100) => 
  api.get(`/campaigns?skip=${skip}&limit=${limit}`);

export const getCampaign = (campaignId) => 
  api.get(`/campaigns/${campaignId}`);

export const createCampaign = (campaignData) => 
  api.post('/campaigns', campaignData);

export const sendCampaign = (campaignId) => 
  api.post(`/campaigns/${campaignId}/send`);

export const createAutomatedCampaigns = () => 
  api.post('/campaigns/automated/high-risk');

// Dashboard
export const getDashboardMetrics = () => 
  api.get('/dashboard');

export default api;
