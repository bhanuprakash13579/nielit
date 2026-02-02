import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../utils/api';

const Dashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState({
        inventory: 0,
        batches: 0,
        content_total: 0,
        content_practical: 0,
        content_pedagogy: 0,
        pending_syncs: 0
    });

    useEffect(() => {
        const fetchStats = async () => {
            if (!user) return;
            try {
                const res = await fetch(`${API_BASE_URL}/api/v1/dashboard/stats`, {
                    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    setStats(data);
                }
            } catch (e) {
                console.error("Stats fetch failed", e);
            }
        };
        fetchStats();
    }, [user]);

    const statCards = [
        { label: 'Total Inventory Kits', value: stats.inventory, change: 'Live Count', color: 'bg-blue-500' },
        { label: 'Active Batches', value: stats.batches, change: 'Running', color: 'bg-green-500' },

        // RFP Specific Content Counters (Clause 4.7)
        { label: 'Practical Videos', value: `${stats.content_practical}/100`, change: 'Target: 100', color: 'bg-indigo-500' },
        { label: 'Pedagogy Videos', value: `${stats.content_pedagogy}/30`, change: 'Target: 30', color: 'bg-purple-500' },
    ];

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-800">Executive Dashboard</h1>
                <p className="text-slate-500">Welcome back, {user?.full_name || 'Administrator'} (Role: {user?.role})</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {statCards.map((stat, index) => (
                    <div key={index} className="glass p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`w-2 h-2 rounded-full ${stat.color}`}></div>
                            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{stat.change}</span>
                        </div>
                        <h3 className="text-3xl font-bold text-slate-800 mb-1">{stat.value}</h3>
                        <p className="text-sm font-medium text-slate-500">{stat.label}</p>
                    </div>
                ))}
            </div>

            {/* Milestone Tracking (Verification Section 5 & 9) */}
            <div className="glass p-6 rounded-xl shadow-sm mb-8 border-l-4 border-green-500">
                <div className="flex justify-between items-center">
                    <div>
                        <h3 className="text-lg font-bold text-slate-800">Project Execution Phases (RFP Section 5)</h3>
                        <p className="text-sm text-slate-500">Concurrent Execution Tracking</p>
                    </div>
                    <div className="text-right">
                        <span className="text-2xl font-bold text-green-600">Phase 1</span>
                        <div className="text-xs text-slate-400">Mobilization & Setup</div>
                    </div>
                </div>
                <div className="mt-6 flex items-center gap-4">
                    {['Phase 1: Mobilization', 'Phase 2: Training', 'Phase 3: Assessment', 'Phase 4: Handoff'].map((step, i) => (
                        <div key={step} className="flex-1">
                            <div className={`h-2 rounded-full mb-2 ${i === 0 ? 'bg-green-500' : 'bg-slate-200'}`}></div>
                            <div className={`text-xs text-center font-medium ${i === 0 ? 'text-green-700' : 'text-slate-400'}`}>{step}</div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Audit Logs Mock */}
                <div className="glass p-6 rounded-xl">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Recent Audit Activity</h3>
                    <div className="space-y-4">
                        {stats.recent_logs && stats.recent_logs.length > 0 ? (
                            stats.recent_logs.map((log, i) => (
                                <div key={i} className="flex items-center justify-between py-2 border-b border-slate-50 last:border-0">
                                    <span className="text-sm font-medium text-slate-800">{log.action}</span>
                                    <span className="text-xs text-slate-500">{log.user} • {log.time}</span>
                                </div>
                            ))
                        ) : (
                            <div className="text-sm text-slate-400 italic">No recent activity</div>
                        )}
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="glass p-6 rounded-xl">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Quick Actions</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <button className="btn btn-secondary text-sm">Download Full Report</button>
                        <button className="btn btn-secondary text-sm">System Health Check</button>
                        <button className="btn btn-secondary text-sm">Manage API Tokens</button>
                        <button className="btn btn-secondary text-sm">View Integration Logs</button>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default Dashboard;
