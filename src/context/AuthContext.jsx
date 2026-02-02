import React, { createContext, useContext, useState, useEffect } from 'react';
import { ROLES } from '../utils/constants';
import { API_BASE_URL } from '../utils/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        // Validate token and get user info on load
        const initAuth = async () => {
            if (token) {
                try {
                    // In a real app, I would call a /me endpoint here.
                    // For now, I decode the token payload if I had a jwt decode lib or just persist user in localStorage too.
                    // Let's persist user in localStorage for simplicity in this prototype.
                    const storedUser = localStorage.getItem('user');
                    if (storedUser) {
                        setUser(JSON.parse(storedUser));
                    }
                } catch (error) {
                    console.error("Auth init failed", error);
                    logout();
                }
            }
            setLoading(false);
        };
        initAuth();
    }, [token]);

    const login = async (username, password) => {
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_BASE_URL}/api/v1/auth/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            const accessToken = data.access_token;

            localStorage.setItem('token', accessToken);
            setToken(accessToken);

            // Hack: For prototype, determining role based on username since /me endpoint isn't fully set up with return model
            // In production, decode JWT or call /me
            let role = ROLES.PROJECT_ADMIN;
            let name = "Project Admin";
            if (username === 'superadmin') {
                role = ROLES.SUPER_ADMIN;
                name = "Super Admin";
            }

            const userObj = { username, role, name };
            setUser(userObj);
            localStorage.setItem('user', JSON.stringify(userObj));

            return userObj;
        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading, token }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
