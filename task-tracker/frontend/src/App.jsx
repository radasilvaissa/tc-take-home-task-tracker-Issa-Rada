// importing React
import React from 'react';
// importing routing tools
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// importing pages
import Dashboard from './pages/Dashboard';
import CreateTask from './pages/CreateTask';
import EditTask from './pages/EditTask';

// default app being exported
// where pages are exported as well
function App() {
  return (
  <Router>
    <Routes>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/create-task" element={<CreateTask />} />
      {/** to identify tasks, we give them specific ids to know what to edit */}
      <Route path="/edit-task/:id" element={<EditTask />} />        
      <Route path="/" element ={<Navigate to="/dashboard"/>} />
    </Routes>
  </Router>
  ); 
}

export default App;