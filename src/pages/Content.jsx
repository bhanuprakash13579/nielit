import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const Content = () => {
    const [contents, setContents] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const { token } = useAuth();

    useEffect(() => {
        fetchContent();
    }, []);

    const fetchContent = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/content/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setContents(data);
            }
        } catch (error) {
            console.error("Failed to fetch content", error);
        }
    };


    const [newItem, setNewItem] = useState({
        title: '',
        category: 'Practical',
        duration_minutes: '',
        tags: '',
        has_safety_checklist: false,
        has_troubleshooting: false,
        has_assessment_cues: false,
        quality_checked: false
    });

    const handleAddItem = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/v1/content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(newItem)
            });
            if (response.ok) {
                setShowModal(false);
                setNewItem({ title: '', category: 'Practical', duration_minutes: '', tags: '' });
                fetchContent();
            }
        } catch (error) {
            console.error("Failed to add content", error);
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">Digital Content Admin</h1>
                    <p className="text-slate-500">Manage Practical & Pedagogy Videos.</p>
                </div>
                <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                    <span className="mr-2">+</span> Add Content
                </button>
            </div>

            <div className="glass rounded-xl overflow-hidden shadow-sm">
                <table className="w-full">
                    <thead className="bg-slate-50">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Title</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Category</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Duration</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Quality Flags</th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Approval</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {contents.map((item) => (
                            <tr key={item.id} className="hover:bg-slate-50">
                                <td className="px-6 py-4 text-sm font-medium text-slate-800">{item.title}</td>
                                <td className="px-6 py-4 text-sm text-slate-500">{item.category}</td>
                                <td className="px-6 py-4 text-sm text-slate-500">{item.duration_minutes} mins</td>
                                <td className="px-6 py-4 text-sm">
                                    <div className="flex gap-1">
                                        {item.quality_checked && <span className="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded border border-green-200" title="Quality Checked">QC</span>}
                                        {item.has_safety_checklist && <span className="px-1.5 py-0.5 bg-blue-100 text-blue-700 text-xs rounded border border-blue-200" title="Safety Checklist">Safe</span>}
                                        {item.has_troubleshooting && <span className="px-1.5 py-0.5 bg-amber-100 text-amber-700 text-xs rounded border border-amber-200" title="Troubleshooting">Trbl</span>}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm">
                                    <div className="flex items-center gap-2">
                                        <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-semibold">{item.approval_status}</span>
                                        {item.ndu_reference_id ? (
                                            <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold" title={item.ndu_reference_id}>Synced</span>
                                        ) : (
                                            <button
                                                className="text-xs text-primary-600 border border-primary-200 px-2 py-1 rounded hover:bg-primary-50"
                                                onClick={async () => {
                                                    try {
                                                        const res = await fetch(`http://localhost:8000/api/v1/integration/sync/content/${item.id}`, {
                                                            method: 'POST',
                                                            headers: { 'Authorization': `Bearer ${token}` }
                                                        });
                                                        if (res.ok) fetchContent();
                                                    } catch (e) {
                                                        console.error("Sync failed", e);
                                                    }
                                                }}
                                            >
                                                Sync NDU
                                            </button>
                                        )}
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {contents.length === 0 && (
                            <tr><td colSpan="4" className="text-center py-8 text-slate-500">No content available.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
                        <h2 className="text-xl font-bold mb-4">Add New Content</h2>
                        <form onSubmit={handleAddItem} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Title</label>
                                <input
                                    type="text"
                                    className="input-field"
                                    value={newItem.title}
                                    onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
                                <select
                                    className="input-field"
                                    value={newItem.category}
                                    onChange={(e) => setNewItem({ ...newItem, category: e.target.value })}
                                >
                                    <option value="Practical">Practical</option>
                                    <option value="Pedagogy">Pedagogy</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Duration (minutes)</label>
                                <input
                                    type="number"
                                    className="input-field"
                                    value={newItem.duration_minutes}
                                    onChange={(e) => setNewItem({ ...newItem, duration_minutes: parseInt(e.target.value) })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Tags (comma separated)</label>
                                <input
                                    type="text"
                                    className="input-field"
                                    value={newItem.tags}
                                    onChange={(e) => setNewItem({ ...newItem, tags: e.target.value })}
                                />
                            </div>
                            <div className="space-y-3 border-t border-slate-100 pt-4 mt-4">
                                <h3 className="text-sm font-semibold text-slate-800">Compliance & Quality (RFP Mandatory)</h3>
                                <div className="grid grid-cols-2 gap-3">
                                    <label className="flex items-center space-x-2 text-sm text-slate-600">
                                        <input type="checkbox" checked={newItem.has_safety_checklist} onChange={(e) => setNewItem({ ...newItem, has_safety_checklist: e.target.checked })} />
                                        <span>Safety Checklist</span>
                                    </label>
                                    <label className="flex items-center space-x-2 text-sm text-slate-600">
                                        <input type="checkbox" checked={newItem.has_troubleshooting} onChange={(e) => setNewItem({ ...newItem, has_troubleshooting: e.target.checked })} />
                                        <span>Troubleshooting</span>
                                    </label>
                                    <label className="flex items-center space-x-2 text-sm text-slate-600">
                                        <input type="checkbox" checked={newItem.has_assessment_cues} onChange={(e) => setNewItem({ ...newItem, has_assessment_cues: e.target.checked })} />
                                        <span>Assessment Cues</span>
                                    </label>
                                    <label className="flex items-center space-x-2 text-sm text-slate-600">
                                        <input type="checkbox" checked={newItem.quality_checked} onChange={(e) => setNewItem({ ...newItem, quality_checked: e.target.checked })} />
                                        <span>Quality Checked</span>
                                    </label>
                                </div>
                            </div>
                            <div className="flex justify-end gap-2 mt-6">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Save Content</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Content;
