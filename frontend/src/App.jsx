// MAIN FILE(home screen)

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

  useEffect(() => {
    const loadUser = async() => {
      const savedToken = localStorage.getItem("token");
      console.log(savedToken);
      if (savedToken) {
        const user_ = await get_session_user(savedToken);
        setUser(user_);
        setToken(savedToken)
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

      {!user ? 
      (
        <div>
          <h1>Login Form</h1>
          <LoginForm setToken = {setToken} setUser={setUser}/>

          <h1>Create User Form</h1>
          <CreateUserForm/>
          </div>
      ) : (
        <>
          <div>
            <h3>Logout Button</h3>
            <button onClick={handleLogOut}>
                LogOut
            </button>
          </div>
          <div>
            <h1>Deposit Form</h1>
            <DepositForm/>
          </div>

          <div>
            <h1>Withdraw Form</h1>
            <WithdrawForm/>
          </div>

          <div>
            <h1>Transfer Form</h1>
            <TransferForm/>
          </div>

          <div>
            <h1>Transaction History</h1>
            <TransactionHistoryView/>
          </div>
        </>
      )}
    </div>
  );
}

export default App;