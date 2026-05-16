// OG-MAIN FILE(home screen)

// default imports
// userState -> Components Render -> seEffect
import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

// manual imports
import DepositForm from './components/depositForm'
import WithdrawForm from './components/withdrawForm'
import TransferForm from './components/transferForm'
import CreateUserForm from './components/createUserForm'
import LoginForm from './components/loginForm'
import TransactionHistoryView from './components/transactionHistoryView'

import { get_session_user } from './api/api'

function App() {
  // Stores the currently logged in user
  // handles within page updates
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");
  const [authTab, setAuthTab] = useState("login"); // "login" | "register"
  const [initials, setInitials] = useState("");


  useEffect(() => {
    const loadUser = async() => {
      const savedToken = localStorage.getItem("token");
      console.log(savedToken);
      if (savedToken) {
        try {
          const user_ = await get_session_user(savedToken);
          setUser(user_);
          setToken(savedToken);
          setInitials(user?.name
            ? user.name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase()
            : "?");
        } catch {
          localStorage.removeItem("token");
        }
      }
    };

    loadUser();
  }, []);

  const handleLogOut = () => {
    setUser(null)
    setToken("");
    localStorage.removeItem("token");
  };

  return (
    <div>
      {/* ── Header ── */}
      <header className="app-header">
        <div className="brand">
          <div className="brand-mark">V</div>
          <div>
            <div className="brand-name">Vault</div>
            <div className="brand-sub">Private Banking</div>
          </div>
        </div>
 
        {user && (
          <div className="header-right">
            <div className="user-pill">
              <div className="user-avatar">{initials}</div>
              <span className="user-name">{user.name || user.email}</span>
            </div>
            <button className="ghost" onClick={handleLogOut} style={{ padding: '8px 18px' }}>
              Sign out
            </button>
          </div>
        )}
      </header>
 
      {/* ── Auth Screen ── */}
      {!user ? (
        <div className="auth-screen">
          <div className="auth-container">
            <div className="auth-headline">
              <h1>Welcome back<span className="gold-dot">.</span></h1>
              <p>SECURE · PRIVATE · TRUSTED</p>
            </div>
 
            <div className="auth-tabs">
              <div
                className={`auth-tab ${authTab === "login" ? "active" : ""}`}
                onClick={() => setAuthTab("login")}
              >
                Sign In
              </div>
              <div
                className={`auth-tab ${authTab === "register" ? "active" : ""}`}
                onClick={() => setAuthTab("register")}
              >
                Open Account
              </div>
            </div>
 
            <div className="auth-card">
              {authTab === "login"
                ? <LoginForm setToken={setToken} setUser={setUser} />
                : <CreateUserForm />
              }
            </div>
          </div>
        </div>
      ) : (
        /* ── Dashboard ── */
        <div className="dashboard">
          {/* Welcome banner */}
          <div className="welcome-banner">
            <div>
              <div className="greeting">Good day</div>
              <h2>{user.name || "Valued Client"}</h2>
              <p className="subtext">{user.email}</p>
            </div>
          </div>
 
          {/* Deposit */}
          <div className="action-card">
            <div className="action-card-header">
              <div>
                <div className="action-card-title">Deposit</div>
              </div>
              <div className="action-card-icon">↓</div>
            </div>
            <DepositForm />
          </div>
 
          {/* Withdraw */}
          <div className="action-card">
            <div className="action-card-header">
              <div>
                <div className="action-card-title">Withdraw</div>
              </div>
              <div className="action-card-icon">↑</div>
            </div>
            <WithdrawForm />
          </div>
 
          {/* Transfer */}
          <div className="action-card">
            <div className="action-card-header">
              <div>
                <div className="action-card-title">Transfer</div>
              </div>
              <div className="action-card-icon">⇄</div>
            </div>
            <TransferForm />
          </div>
 
          {/* Transaction History */}
          <div className="history-card">
            <div className="history-card-header">
              <div className="history-card-title">Transaction History</div>
            </div>
            <TransactionHistoryView />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;