import React from 'react';

// Import routing tools
// Link = creates clickable links to different pages
// useLocation = gets current page URL
import { Link, useLocation } from 'react-router-dom';
// import css
import './Sidebar.css';

// sidebar rendering
function Sidebar() {
    // useLocation = gets current page URL
    const location = useLocation();
    const currentPath = location.pathname;

    // Determine which link should be highlighted
    let dashboardClass = 'sidebar-link';
    if (currentPath === '/dashboard') {
        dashboardClass = 'sidebar-link active';
    }

    let createTaskClass = 'sidebar-link';
    if (currentPath === '/create-task') {
        createTaskClass = 'sidebar-link active';
    }

    // Return JSX (what shows on screen)
    return (
        <div className="sidebar">
            <h2 className="sidebar-title">Task Tracker</h2>
            <nav className="sidebar-nav">
                <Link to="/dashboard" className={dashboardClass}>
                    Dashboard
                </Link>
                <Link to="/create-task" className={createTaskClass}>
                    Add Task
                </Link>
            </nav>
        </div>
    );
}

export default Sidebar;