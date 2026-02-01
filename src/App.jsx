import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import DashboardLayout from './components/layout/DashboardLayout';
import ProtectedRoute from './components/layout/ProtectedRoute';
import Inventory from './pages/Inventory';
import Training from './pages/Training';
import Content from './pages/Content';
import Users from './pages/Users';
import { ROLES } from './utils/constants';

// Placeholder Dashboard


const NotFound = () => <div className="p-8 text-center text-red-500 text-xl font-bold">404 Not Found</div>;

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/training" element={<Training />} />
              <Route path="/content" element={<Content />} />
              <Route path="/users" element={<Users />} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Route>

          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
