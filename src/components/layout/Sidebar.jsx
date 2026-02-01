import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ROLES } from '../../utils/constants';

const Sidebar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navItems = [
        { name: 'Dashboard', path: '/dashboard', icon: '📊' },
        { name: 'Inventory', path: '/inventory', icon: '📦' },
        { name: 'Training', path: '/training', icon: '🎓' },
        { name: 'Content', path: '/content', icon: '🎬' },
        { name: 'Users', path: '/users', icon: '👥' },
    ];

    return (
        <aside className="w-64 bg-white border-r border-slate-200 h-screen sticky top-0 flex flex-col p-6">
            <div className="flex items-center gap-2 mb-10 text-primary-600">
                <div className="w-8 h-8 rounded-lg bg-primary-600"></div>
                <h2 className="text-xl font-bold text-slate-800">SAMARTH</h2>
            </div>

            <nav className="flex-1 flex flex-col gap-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) => `
              flex items-center gap-3 px-4 py-3 rounded-md transition-all duration-200
              ${isActive ? 'bg-primary-50 text-primary-600 font-semibold' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'}
            `}
                    >
                        <span>{item.icon}</span>
                        {item.name}
                    </NavLink>
                ))}
            </nav>

            <div className="mt-auto border-t border-slate-200 pt-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-full bg-secondary-500 flex items-center justify-center text-white font-bold">
                        {user?.name?.charAt(0) || 'U'}
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-slate-800">{user?.name}</p>
                        <p className="text-xs text-slate-500">{user?.role}</p>
                    </div>
                </div>
                <button
                    onClick={handleLogout}
                    className="btn w-full justify-start text-red-500 hover:bg-red-50 hover:text-red-600 px-0 pl-1"
                >
                    <span className="mr-2">🚪</span> Sign Out
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
