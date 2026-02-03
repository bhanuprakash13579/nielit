import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../utils/api';

const Training = () => {
    const [trainings, setTrainings] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const { token } = useAuth();

    useEffect(() => {
        fetchTrainings();
    }, []);

    const fetchTrainings = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/training/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setTrainings(data);
            }
        } catch (error) {
            console.error("Failed to fetch trainings", error);
        }
    };

    const getStatusColor = (status) => {
        return status === 'Upcoming'
            ? 'bg-blue-100 text-blue-700'
            : 'bg-green-100 text-green-700';
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">Training Management</h1>
                    <p className="text-slate-500">Manage courses and track participants.</p>
                </div>
                <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                    <span className="mr-2">+</span> Schedule Training
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trainings.map(training => (
                    <div key={training.id} className="glass p-6 rounded-xl flex flex-col shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between mb-4">
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(training.status)}`}>
                                {training.status}
                            </span>
                            <span className="text-sm text-slate-500">
                                {training.date}
                            </span>
                        </div>

                        <h3 className="text-xl font-bold mb-2 text-slate-800">{training.title}</h3>
                        <p className="text-slate-500 mb-6 flex-1">Instructor: {training.instructor}</p>

                        <div className="flex justify-between items-center pt-4 border-t border-slate-100">
                            <span className="text-sm font-medium text-slate-700">👥 {training.participants_count} Participants</span>
                            <div className="flex gap-2">
                                {training.ndu_mapping_id ? (
                                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">NDU Synced</span>
                                ) : (
                                    <button
                                        className="text-xs text-primary-600 border border-primary-200 px-2 py-1 rounded hover:bg-primary-50"
                                        onClick={async () => {
                                            try {
                                                const res = await fetch(`${API_BASE_URL}/api/v1/integration/sync/training/${training.id}`, {
                                                    method: 'POST',
                                                    headers: { 'Authorization': `Bearer ${token}` }
                                                });
                                                if (res.ok) fetchTrainings();
                                            } catch (e) { console.error("Sync failed", e); }
                                        }}
                                    >
                                        Sync NDU
                                    </button>
                                )}
                                {/* Clause 4.3: Attendance Visibility */}
                                <button className="text-xs font-bold text-slate-500 uppercase tracking-wide px-2 hover:text-slate-700" onClick={() => alert("Compliance: Showing Attendance Sheet")}>
                                    View Attendance
                                </button>
                                <button
                                    className="text-primary-600 font-medium hover:text-primary-800 text-sm"
                                    onClick={() => alert(`Details:\nProgram: ${training.title}\nInstructor: ${training.instructor}\nParticipants: ${training.participants_count}\nStatus: ${training.status}\n\n(Batch View to be implemented in Phase 2)`)}
                                >
                                    View Details
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
                {trainings.length === 0 && (
                    <div className="col-span-full text-center text-slate-500 py-12">
                        No trainings found.
                    </div>
                )}
            </div>

            {/* Simple Modal Implementation */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
                        <h2 className="text-xl font-bold mb-4 text-slate-800">Schedule New Training</h2>
                        <form onSubmit={(e) => {
                            e.preventDefault();
                            const formData = new FormData(e.target);
                            const newTraining = {
                                title: formData.get('title'),
                                instructor: formData.get('instructor'),
                                date: formData.get('date'),
                                participants_count: 0,
                                status: 'Upcoming' // Default status
                            };

                            (async () => {
                                try {
                                    const response = await fetch(`${API_BASE_URL}/api/v1/training/`, {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'Authorization': `Bearer ${token}`
                                        },
                                        body: JSON.stringify(newTraining)
                                    });
                                    if (response.ok) {
                                        fetchTrainings();
                                        setShowModal(false);
                                    } else {
                                        const err = await response.json();
                                        alert("Failed: " + (err.detail || "Error creating training"));
                                    }
                                } catch (error) {
                                    console.error("Failed to schedule training", error);
                                    alert("Network Error: Could not schedule training");
                                }
                            })();
                        }} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Title</label>
                                <input name="title" type="text" className="input-field" required />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Instructor</label>
                                <input name="instructor" type="text" className="input-field" required />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Date</label>
                                <input name="date" type="date" className="input-field" required />
                            </div>
                            <div className="flex justify-end gap-2 mt-6">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Schedule</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Training;
