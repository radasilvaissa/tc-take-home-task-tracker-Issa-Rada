// import React
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TaskCard.css';

// funciton to display the task card
// props = data passed from parent component (Dashboard)
function TaskCard(props) {
    // get task data from props
    const task = props.task;
    // onDelete function from props (passed from Dashboard)
    const onDelete = props.onDelete;
    // useNavigate = function to change pages
    const navigate = useNavigate();

    // handleEdit = runs when user clicks edit button
    function handleEdit() {
        // navigate to edit page with task ID
        navigate('/edit-task/' + task.id);
    }

    // handleDelete = runs when user clicks delete button
    function handleDelete() {
        // call the onDelete function passed from Dashboard
        onDelete(task.id);
    }

    // format due date to be readable
    let dueDateText = '';
    if (task.due_date) {
        const date = new Date(task.due_date);
        dueDateText = date.toLocaleDateString();
    }

    // card status as completed or pending, changing css depending on it
    let cardClass = 'task-card';
    if (task.status === 'completed') {
        cardClass = 'task-card completed';
    } else {
        cardClass = 'task-card pending';
    }

    // return for the task card
    return (
        <div className={cardClass}>
            {/* task title */}
            <h3 className="task-title">{task.title}</h3>
            
            {/* task info -> category, importance, and due date */}
            <div className="task-info">
                <span className="task-category">{task.category}</span>
                <span className="task-importance">{task.importance}/5</span>
                {dueDateText ? <span className="task-due-date">Due: {dueDateText}</span> : null}
            </div>
            
            {/* buttons to delete or edit */}
            <div className="task-actions">
                <button onClick={handleEdit} className="task-button edit-button">
                    Edit
                </button>
                <button onClick={handleDelete} className="task-button delete-button">
                    Delete
                </button>
            </div>
        </div>
    );
}

export default TaskCard;