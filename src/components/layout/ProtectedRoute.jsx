import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ allowedRoles = [] }) => {
    const { user, loading } = useAuth();

    if (loading) {
        return <div className="flex justify-center items-center h-screen text-slate-500">Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
        return (
            <div className="flex flex-col items-center justify-center h-screen text-center p-8">
                <h1 className="text-4xl font-bold text-slate-800 mb-4">403 Forbidden</h1>
                <p className="text-slate-500">You do not have permission to view this page.</p>
            </div>
        );
    }

    return <Outlet />;
};

export default ProtectedRoute;
