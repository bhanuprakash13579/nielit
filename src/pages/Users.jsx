import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const Users = () => {
    const [users, setUsers] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const { token, user: currentUser } = useAuth();

    // Form State
    const [newUser, setNewUser] = useState({
        username: '',
        password: '',
        full_name: '',
        role: 'ADMIN'
    });

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/users/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                setUsers(await response.json());
            }
        } catch (error) {
            console.error("Failed to fetch users", error);
        }
    };

    const handleAddUser = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(newUser)
            });
            if (response.ok) {
                setShowModal(false);
                setNewUser({ username: '', password: '', full_name: '', role: 'ADMIN' });
                fetchUsers();
            } else {
                alert("Failed to create user");
            }
        } catch (error) {
            console.error("Error creating user", error);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            const response = await fetch(`http://localhost:8000/api/v1/auth/users/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                setUsers(users.filter(u => u.id !== id));
            } else {
                alert("Failed to delete user (Only Super Admin can delete)");
            }
        } catch (error) {
            console.error("Error deleting user", error);
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">User Management</h1>
                    <p className="text-slate-500">Manage system access and roles.</p>
                </div>
                <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                    <span className="mr-2">+</span> Add User
                </button>
            </div>

            <div className="glass rounded-xl overflow-hidden shadow-sm">
                <table className="w-full">
                    <thead className="bg-slate-50">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">User</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Role</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Status</th>
                            <th className="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {users.map((u) => (
                            <tr key={u.id} className="hover:bg-slate-50">
                                <td className="px-6 py-4">
                                    <div className="flex items-center">
                                        <div className="h-8 w-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center font-bold mr-3">
                                            {u.username.charAt(0).toUpperCase()}
                                        </div>
                                        <div>
                                            <div className="text-sm font-medium text-slate-800">{u.full_name}</div>
                                            <div className="text-xs text-slate-500">@{u.username}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${u.role === 'SUPER_ADMIN' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'}`}>
                                        {u.role}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                        {u.is_active ? 'Active' : 'Inactive'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    {currentUser?.role === 'SUPER_ADMIN' && u.id !== currentUser.id && (
                                        <button onClick={() => handleDelete(u.id)} className="text-red-500 hover:text-red-700 text-sm font-medium">Delete</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
                        <h2 className="text-xl font-bold mb-4">Add New User</h2>
                        <form onSubmit={handleAddUser} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
                                <input
                                    type="text"
                                    className="input-field"
                                    value={newUser.username}
                                    onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                                <input
                                    type="text"
                                    className="input-field"
                                    value={newUser.full_name}
                                    onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    className="input-field"
                                    value={newUser.password}
                                    onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Role</label>
                                <select
                                    className="input-field"
                                    value={newUser.role}
                                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                                >
                                    <option value="ADMIN">Admin</option>
                                    <option value="SUPER_ADMIN">Super Admin</option>
                                </select>
                            </div>
                            <div className="flex justify-end gap-2 mt-6">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Create User</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Users;
