// useState lets a component remember a value when you update it with the setter
// useEffect lets a component run code when the page loads, like fetching tasks
import React, {useState, useEffect} from "react"; 
// importing components
import Sidebar from "../components/Sidebar";
import TaskCard from "../components/TaskCard";
// import css 
import "./Dashboard.css";

// funciton to render the dahsboard
function Dashboard() {
    // empty array as the tasks initially
    const [tasks, setTasks] = useState([]);
    // while fetching tasks, it is showing the "loading" state 
    const [loading, setLoading] = useState(true); 
    // determines how to sort tasks
    // default is by due date 
    const [sortBy, setSortBy] = useState("due_date");
    // fetches tasks as soon as the component first loads! 
    // first bc its empty
    useEffect(function() {
        fetchTasks(); 
    }, []); 

    // function to fetch the tasks
    // async as it waits for backend response
    async function fetchTasks() {
        // get request to fetch the tasks from this url (api req)
        const url = "http://localhost:5000/api/tasks"; 
        const options = {
            method: "GET", 
        }; 
        // fetch sends the request to the backend and waits for the response
        const response = await fetch(url, options); 

        if (response.ok) {
            const data = await response.json(); 
            setTasks(data); 
        }
        // done loading as the tasks have been fetched
        setLoading(false ); 
    }

    // funciton to filter the tasks
    // if it appears in the search or not, so if the title includes anything from search bar
    function filterTasks() {
        const filtered = []; 
        // loop through the tasks
        for (let i = 0; i < tasks.length; i++) {
            const task = tasks[i]; 
            // convert to lower case
            const taskTitle = task.title.toLowerCase(); 
            const search = searchTerm.toLowerCase(); 

            if (taskTitle.includes(search)) {
                filtered.push(task); 
            }
        }
        return filtered; 
    }

    // function to sort tasks based on a criteria
    function sortTasks(taskList) {
        // copy the array so we don't modify the original
        const sorted = [...taskList]; 
        // sort by due dates
        if (sortBy == "due_date") {
            sorted.sort(function(a, b) {
                const dateA = new Date(a.due_date || 0); 
                const dateB = new Date(b.due_date || 0); 
                return dateA - dateB; 
            }); 
        }

        // sort by importance
        else if (sortBY == "importance") {
            sorted.sort(function(a, b) {
                return b.importance - a.importance; 
            }); 
        }
        return sorted; 
    }

    // funciton to delete a task
    async function handleDelete(taskId) {
        const confirmed = window.confirm("Are you sure you want to delete the task?"); 

        if (confirmed) {
            const url = "http://localhost:5000/api/tasks/" + taskId;
            const options = {
                method: "DELETE", 
            }; 

            const response = await fetch(url, options); 

            // if deleting worked
            if (response.ok) {
                const newTasks = []; 
                for (let i = 0; i < tasks.length; i++) {
                    if (tasks[i].id !== taskId) {
                        newTasks.push(tasks[i]); 
                    }
                }
                setTasks(newTasks); 
            }
        }
    }

    // runs when the user types in the search box
    // event.target.value is the actual text typed in the search box
    function handleSearchChange(event) {
        const newSearchTerm = event.target.value; 
        setSearchTerm(newSearchTerm); 
    }

    // handles a change in the sorting dropdown
    function handleSortingChange(event) {
        const newSortBy = event.target.value; 
        setSortBy(newSortBy); 
    }

    // shows loading while fetching backend info
    if (loading) {
        return <div>Loading ...</div>; 
    }

    const filteredtasks = filterTasks(); 
    const sortedTasks = sortTasks(filteredTasks); 

    // return jsx funciton
      return (
        <div className="dashboard-container">
            {/** calling the actual sidebar component here */}
            <Sidebar />
            
            {/** dashboard design */}
            <div className="dashboard-main">
                <div className="dashboard-header">
                    <h1>Dashboard</h1>
                    
                    {/* search and sort controls */}
                    <div className="dashboard-controls">
                        <input
                            type="text"
                            placeholder="Search tasks..."
                            value={searchTerm}
                            onChange={handleSearchChange}
                            className="search-input"
                        />
                        <select
                            value={sortBy}
                            onChange={handleSortChange}
                            className="sort-select"
                        >
                            <option value="due_date">Sort by Due Date</option>
                            <option value="importance">Sort by Importance</option>
                            <option value="category">Sort by Category</option>
                        </select>
                    </div>
                </div>
                
                {/* rendering tasks in a readability list */}
                {/* displaying in a task grid */}
                <div className="tasks-grid">
                    {sortedTasks.length === 0 ? (
                        <p>No tasks found</p>
                    ) : (
                        // map through tasks and create TaskCard for each
                        // renders tasks in a readable list/grid
                        sortedTasks.map(function(task) {
                            return (
                                <TaskCard
                                    key={task.id}
                                    task={task}
                                    onDelete={handleDelete}
                                />
                            );
                        })
                    )}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
