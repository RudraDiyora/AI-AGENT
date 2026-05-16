// REVAMPED MAIN FILE(home screen)

// default imports
// userState -> Components Render -> seEffect
import { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import './App.css'

// manual imports
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';

import { loadSessionUser } from './api/api';

function App() {
  // Stores the currently logged in user
  // handles within page updates
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");

  useEffect(() => {
    console.log('RENDERING APP.JS');
  const loadUser = async() => { await loadSessionUser({setUser, setToken})};
    loadUser();
  }, []);

  const handleLogOut = () => {
    setUser(null)
    setToken("");
    localStorage.removeItem("token");
  };

  return (
    <Routes>
      <Route path="/login"     element={user ? <Navigate to="/dashboard" /> : <LoginPage setUser={setUser} setToken={setToken} />} />
      <Route path="/dashboard" element={user ? <DashboardPage user={user} onLogout={handleLogOut} t={token} /> : <Navigate to="/login" />} />
      <Route path="*"          element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;