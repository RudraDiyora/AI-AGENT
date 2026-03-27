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


function App() {
  return (
    <div>
      <h1>Bank App</h1>
      <DepositForm userID={"57c4ec95-cd10-4060-af44-dd853c18df2e"}/>
      <h1>Bank App</h1>
      <WithdrawForm userID={"57c4ec95-cd10-4060-af44-dd853c18df2e"}/>
    </div>
  );
}

export default App;