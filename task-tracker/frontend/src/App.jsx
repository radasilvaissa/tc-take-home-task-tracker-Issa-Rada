import React from 'react';
// importing routing tools
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// importing authentication context
import { AuthProvider, AuthContext } from './auth/authentication';
// importing pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CreateTask from './pages/CreateTask';
import Profile from './pages/Profile';

// function to show the pages, only if user is auth
function PrivateRoute(props) {
  // getting the children/components aka the page we want to display from props
  const children = props.children; 

  // get authenticaiton informaiton to show if auth
  const authContext = React.useContext(AuthContext); 
  const isAuthenticated = authContext.isAuthenticated; 
  const loading = authContext.loading; 

  // if still checking, show loading
  if (loading) {
    return <div>Loading...</div>; 
  }

  // if logged in, show the page
  if (isAuthenticated) {
    return children; 
  } else {
    return <Navigate to="/login"/>; 
  }
}

// default app being exported
// where pages are exported as well
function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/create-task" element={<PrivateRoute><CreateTask /></PrivateRoute>} />
          <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
          <Route path="/" element ={<Navigate to="/dashboard"/>} />
        </Routes>
      </Router>
      </AuthProvider>
  ); 
}

export default App;