// MAIN FILE(home screen)

// default imports
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

// manual imports
import DepositForm from './components/depositForm'
import WithdrawForm from './components/withdrawForm'
import TransferFrom from './components/transferForm'
import CreateUserForm from './components/createUserForm'



function App() {
  return (
    <div>

      <div>
        <h1>Create User Form</h1>
        <CreateUserForm/>
      </div>

      <div>
        <h1>Deposit From</h1>
        <DepositForm userID={"18a27054-d535-43bd-8f96-b525b8ed9810"}/>
      </div>

      <div>
        <h1>Withdraw Form</h1>
        <WithdrawForm userID={"18a27054-d535-43bd-8f96-b525b8ed9810"}/>
      </div>

      <div>
        <h1>Transfer Form</h1>
        <TransferFrom userID={"18a27054-d535-43bd-8f96-b525b8ed9810"}/>
      </div>
    </div>
  );
}

export default App;