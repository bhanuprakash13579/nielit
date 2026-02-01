export const ROLES = {
    SUPER_ADMIN: 'SUPER_ADMIN',
    PROJECT_ADMIN: 'PROJECT_ADMIN',
};

export const MOCK_USERS = [
    {
        id: 1,
        username: 'superadmin',
        password: 'password123',
        role: ROLES.SUPER_ADMIN,
        name: 'Super Admin User'
    },
    {
        id: 2,
        username: 'admin',
        password: 'password123',
        role: ROLES.PROJECT_ADMIN,
        name: 'Project Admin User'
    }
];

export const MOCK_INVENTORY = [
    { id: 1, name: 'Dell XPS 13', category: 'Laptops', quantity: 15, status: 'In Stock', lastUpdated: '2024-01-20' },
    { id: 2, name: 'MacBook Pro 16', category: 'Laptops', quantity: 5, status: 'Low Stock', lastUpdated: '2024-01-25' },
    { id: 3, name: 'Logitech MX Master 3', category: 'Peripherals', quantity: 30, status: 'In Stock', lastUpdated: '2024-01-15' },
    { id: 4, name: 'Dell 27" Monitor', category: 'Monitors', quantity: 0, status: 'Out of Stock', lastUpdated: '2024-01-10' },
    { id: 5, name: 'HDMI Cable (2m)', category: 'Cables', quantity: 50, status: 'In Stock', lastUpdated: '2024-01-05' },
];

export const MOCK_TRAININGS = [
    { id: 1, title: 'React Basics', instructor: 'John Doe', date: '2024-02-15', participants: 12, status: 'Upcoming' },
    { id: 2, title: 'Advanced CSS', instructor: 'Jane Smith', date: '2024-02-10', participants: 25, status: 'Completed' },
    { id: 3, title: 'Project Management', instructor: 'Mike Johnson', date: '2024-03-01', participants: 5, status: 'Upcoming' },
];
