// useState lets a component remember a value when you update it with the setter
import React, { useState } from 'react';

import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import './CreateTask.css';

//function to render createTask
function CreateTask() {
    // storing all the stubs
    const [title, setTitle] = useState('');
    const [importance, setImportance] = useState(1);
    const [category, setCategory] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [status, setStatus] = useState('pending');
    
    // useNavigate = function to change pages
    const navigate = useNavigate();

    // handleSubmit
    // when a user creates the task, it posts it in the backend
    async function handleSubmit(event) {
        event.preventDefault();
        
        const url = 'http://localhost:5000/api/tasks';
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                importance: parseInt(importance),
                category: category,
                due_date: dueDate,
                status: status,
            }),
        };
        
        const response = await fetch(url, options);
        
        if (response.ok) {
            navigate('/dashboard');
        }
    }

    // Handle functions changing each field
    function handleTitleChange(event) {
        setTitle(event.target.value);
    }

    function handleImportanceChange(event) {
        setImportance(event.target.value);
    }

    function handleCategoryChange(event) {
        setCategory(event.target.value);
    }

    function handleDueDateChange(event) {
        setDueDate(event.target.value);
    }

    function handleStatusChange(event) {
        setStatus(event.target.value);
    }

    return (
        <div className="create-task-container">
            <Sidebar />
            <div className="create-task-main">
                <h1>Create New Task</h1>
                <form onSubmit={handleSubmit} className="create-task-form">
                    <input
                        type="text"
                        placeholder="Task Title"
                        value={title}
                        onChange={handleTitleChange}
                        required
                        className="form-input"
                    />
                    <select
                        value={importance}
                        onChange={handleImportanceChange}
                        className="form-input"
                    >
                        <option value={1}>Importance: 1</option>
                        <option value={2}>Importance: 2</option>
                        <option value={3}>Importance: 3</option>
                        <option value={4}>Importance: 4</option>
                        <option value={5}>Importance: 5</option>
                    </select>
                    <input
                        type="text"
                        placeholder="Category"
                        value={category}
                        onChange={handleCategoryChange}
                        className="form-input"
                    />
                    <input
                        type="date"
                        value={dueDate}
                        onChange={handleDueDateChange}
                        className="form-input"
                    />
                    <select
                        value={status}
                        onChange={handleStatusChange}
                        className="form-input"
                    >
                        <option value="pending">Status: Pending</option>
                        <option value="completed">Status: Completed</option>
                    </select>
                    <button type="submit" className="submit-button">
                        Create Task
                    </button>
                </form>
            </div>
        </div>
    );
}

export default CreateTask;