// MAIN FILE(home screen)

// default imports
import '../App.css'

// manual imports
import DepositForm from '../components/depositForm'
import WithdrawForm from '../components/withdrawForm'
import TransferForm from '../components/transferForm'
import TransactionHistoryView from '../components/transactionHistoryView'
import { useState } from 'react'


// src/pages/Dashboard.jsx
export default function DashboardPage({ user, onLogout, t }) {

    const initials = user?.name
        ? user.name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase()
        : "?";
    console.log("dashboarddd");
        
    debugger;
    return (
        <div>
        <header className="app-header">
            <div className="brand">
            <div className="brand-mark">V</div>
            <div>
                <div className="brand-name">Vault</div>
                <div className="brand-sub">Private Banking</div>
            </div>
            </div>
            <div className="header-right">
            <div className="user-pill">
                <div className="user-avatar">{initials}</div>
                <span className="user-name">{user?.name || user?.email}</span>
            </div>
            <button className="ghost" onClick={onLogout} style={{ padding: "8px 18px" }}>
                Sign out
            </button>
            </div>
        </header>

        <div className="dashboard">
            <div className="welcome-banner">
            <div>
                <div className="greeting">Good day</div>
                <h2>{user?.name || "Valued Client"}</h2>
                <p className="subtext">{user?.email}</p>
            </div>
            </div>

            <div className="action-card">
            <div className="action-card-header">
                <div className="action-card-title">Deposit</div>
                <div className="action-card-icon">↓</div>
            </div>
            <DepositForm />
            </div>

            <div className="action-card">
            <div className="action-card-header">
                <div className="action-card-title">Withdraw</div>
                <div className="action-card-icon">↑</div>
            </div>
            <WithdrawForm />
            </div>

            <div className="action-card">
            <div className="action-card-header">
                <div className="action-card-title">Transfer</div>
                <div className="action-card-icon">⇄</div>
            </div>
            <TransferForm />
            </div>

            <div className="history-card">
            <div className="history-card-header">
                <div className="history-card-title">Transaction History</div>
            </div>
            <TransactionHistoryView />
            </div>
        </div>
        </div>
    );
}