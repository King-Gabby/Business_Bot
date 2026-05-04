import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import AdminDashboard from './pages/admin/AdminDashboard';
import BusinessOnboarding from './pages/admin/BusinessOnboarding';
import ProductsManager from './pages/admin/ProductsManager';
import SettingsManager from './pages/admin/SettingsManager';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Public Chat Area */}
        <Route path="/" element={<ChatPage />} />
        <Route path="/chat/:businessId" element={<ChatPage />} />

        {/* Admin Area */}
        <Route path="/admin/onboarding" element={<BusinessOnboarding />} />
        <Route path="/admin/:businessId" element={<AdminDashboard />} />
        <Route path="/admin/:businessId/products" element={<ProductsManager />} />
        <Route path="/admin/:businessId/settings" element={<SettingsManager />} />
      </Routes>
    </Router>
  );
};

export default App;
