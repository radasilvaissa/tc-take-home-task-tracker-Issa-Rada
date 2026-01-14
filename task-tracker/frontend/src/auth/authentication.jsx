import React from "react"; 
import { createContext, useState, useEffect } from "react";

export const AuthConcext = createContext(); 

export function AuthProvider(props) {
    // get components inside of props
    const children = props.children; 
    // setting the user, null of nobody
    const [user, setUser] = useState(null);
    // setting isAuthenticated to false if nobody is, true if logged in
    const [isAuthenticated, setIsAuthenticated] = useState(false); 
    // loading is true while we check if the user was logged in before
    const [loading, setLoading] = useState(true); 

    // useEffect runs when the app runs
    useEffect(function () {
        // uses localStorage to check if we saved a user before
        const savedUser = localStorage.getItem("user"); 
        if (savedUser) {
            const userObject = JSON.parse(savedUser); 
            setUser(userObject); 
            setIsAuthenticated(true);
        }

        setLoading(false);
        // empty array to run once the app starts 
    }, []); 

    // functon to log in, sending username and password to backend
    // async bc it pauses while it waits for something
    async function login(username, password) {
        try {
            const url = "http://localhost:5000/api/login";
            const options = {
                methods: "POST", 
                // telling the server we're sending JSON
                headers: {"Content-Type": "application.json"}, 
                credentials: "include",
                body: JSON.stringify({username: username, password: password || ""}), 
            };

            const response = await fetch(url, options);
            if (response.ok) {
                const data = await response.json;

                setUser(data.user); 
                setIsAuthenticated(true); 
                localStorage.setItem("user", JSON.stringify(data.user)); 
                return {success: true}; 
            } else {
                return {sucess: false, error: "Login failed"}; 
            }
        } catch (error) {
            return {sucess: false, error: error.message }; 
        }
    }
    
    function logout() {
        setUser(null); 
        setIsAuthenticated(false); 
        localStorage.removeItem("user"); 
        fetch("http://localhost:5000/api/logout", {
            method: "POST", 
            credentials: "include", 
        }); 
    }

    const value = {
        user: user, 
        isAuthenticated: isAuthenticated, 
        loading: loading, 
        login: login, 
        logout: logout
    }; 

    return (
        <AuthContext.Provider value={value}>
            {children}
            </AuthContext.Provider>
    ); 
}