import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsSubmitting(true);

        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid username or password');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-primary-100 relative overflow-hidden">
            {/* Decorative blobs */}
            <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-secondary-500 blur-3xl opacity-20 rounded-full"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-primary-500 blur-3xl opacity-20 rounded-full"></div>

            <div className="glass max-w-md w-full p-8 rounded-xl shadow-xl z-10">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-primary-600 mb-2">SAMARTH</h1>
                    <p className="text-slate-500">Sign in to your account</p>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="mb-6">
                        <label htmlFor="username" className="block text-sm font-medium text-slate-700 mb-2">Username</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="input-field"
                            placeholder="Enter your username"
                            required
                        />
                    </div>

                    <div className="mb-8">
                        <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input-field"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary w-full"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-slate-500">
                    <p>Demo Credentials:</p>
                    <p>superadmin / password123</p>
                    <p>admin / password123</p>
                </div>
            </div>
        </div>
    );
};

export default Login;
