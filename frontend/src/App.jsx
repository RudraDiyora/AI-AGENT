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

function App() {
  // Stores the currently logged in user
  // handles within page updates
  const [user, setUser] = useState(null);

  // useEffect runs AFTER the component renders -> handles page-to-page refreshes
  useEffect(() => { // triggered upon app reload

    // localStorage is persistent browser storage.
    // getItem("userID") checks if a userID was saved previously.
    // Returns:
    //   - the saved string if it exists
    //   - null if nothing is saved
    const savedUser = localStorage.getItem("user");

    
    // If a saved user exists
    if (savedUser) {
      // Restore the user into React state
      // Updating state causes React to rerender the UI
      setUser(JSON.parse(savedUser));
    }
  //[]	once after first render
  //[user]	whenever user changes
  //no array	every render
  }, []);

  const handleLogOut = () => {
    setUser(null)
    localStorage.removeItem("user");
  };
  
  return (
    <div>

      {!user ? 
      (
        <div>
          <h1>Login Form</h1>
          <LoginForm setUser={setUser}/>

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
            <DepositForm userID={user.user_id}/>
          </div>

          <div>
            <h1>Withdraw Form</h1>
            <WithdrawForm userID={user.user_id}/>
          </div>

          <div>
            <h1>Transfer Form</h1>
            <TransferForm userID={user.user_id}/>
          </div>
        </>
      )}
    </div>
  );
}

export default App;