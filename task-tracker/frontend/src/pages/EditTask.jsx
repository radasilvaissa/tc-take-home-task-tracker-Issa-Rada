import React, { useState, useEffect } from 'react';

import { useParams, useNavigate } from 'react-router-dom';

import Sidebar from '../components/Sidebar';
import './EditTask.css';

// function to edit a task and render it
function EditTask() {
    // useParams = gets URL parameters (task ID from URL)
    const params = useParams();
    const taskId = params.id;
    
    // useState  to store form input values
    const [title, setTitle] = useState('');
    const [importance, setImportance] = useState(3);
    const [category, setCategory] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [status, setStatus] = useState('pending');
    const [loading, setLoading] = useState(true);
    
    // useNavigate = function to change pages
    const navigate = useNavigate();

    // useEffect = runs when component first loads
    // Fetches the task data and fills the form
    useEffect(function() {
        fetchTask();
    }, []);

    // fetchTask = gets task data from backend
    // handled in dashboard with a get request
    async function fetchTask() {
        const url = 'http://localhost:5001/api/tasks/' + taskId;
        const response = await fetch(url);
        
        if (response.ok) {
            const data = await response.json();
            setTitle(data.title);
            setImportance(data.importance);
            setCategory(data.category);
            setDueDate(data.due_date || '');
            setStatus(data.status);
        }
        
        setLoading(false);
    }

    // handleSubmit -> submits the change to the task when the user clicks submit
    async function handleSubmit(event) {
        event.preventDefault();
        
        const url = 'http://localhost:5001/api/tasks/' + taskId;
        const options = {
            method: 'PUT',
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

    // handleDelete -> deletes a task when the user clicks delete
    async function handleDelete() {
        const confirmed = window.confirm('Are you sure you want to delete this task?');
        
        if (confirmed) {
            const url = 'http://localhost:5001/api/tasks/' + taskId;
            const options = {
                method: 'DELETE',
            };
            
            const response = await fetch(url, options);
            
            if (response.ok) {
                navigate('/dashboard');
            }
        }
    }

    // Handle changes for each input
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

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="edit-task-container">
            <Sidebar />
            <div className="edit-task-main">
                <h1>Edit Task</h1>
                <form onSubmit={handleSubmit} className="edit-task-form">
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
                    <div className="edit-task-buttons">
                        <button type="submit" className="submit-button">
                            Save Changes
                        </button>
                        <button type="button" onClick={handleDelete} className="delete-button">
                            Delete Task
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default EditTask;