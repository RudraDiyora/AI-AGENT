import { useState, useEffect } from 'react'

import LoginForm from "../components/loginForm";
import CreateUserForm from "../components/createUserForm";
import { get_session_user, loadSessionUser } from '../api/api'


export default function LoginPage({ setUser, setToken }) {
  const [authTab, setAuthTab] = useState("login");

  const loadUser = async() => { await loadSessionUser({setUser, setToken})};


  // IMPORTANT -> SESSION HANDLING
  useEffect(() => {
    loadUser();
  }, []);

  return (
    <div className="auth-screen">
      <div className="auth-container">
        <div className="auth-headline">
          <h1>Welcome back<span className="gold-dot">.</span></h1>
          <p>SECURE · PRIVATE · TRUSTED</p>
        </div>

        <div className="auth-tabs">
          <div className={`auth-tab ${authTab === "login" ? "active" : ""}`} onClick={() => setAuthTab("login")}>
            Sign In
          </div>
          <div className={`auth-tab ${authTab === "register" ? "active" : ""}`} onClick={() => setAuthTab("register")}>
            Open Account
          </div>
        </div>

        <div className="auth-card">
          {authTab === "login"
            ? <LoginForm setToken={setToken} setUser={setUser} loadUser={loadUser} />
            : <CreateUserForm />}
        </div>
      </div>
    </div>
  );
}