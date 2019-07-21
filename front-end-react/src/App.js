import React from 'react';
// import logo from './logo.svg';
import './App.css';
import Main from './components/Main.js'
import Navbar from './components/Navbar.js'

function App() {
  return (
    <div className="App">
      <Navbar />
      <main class='container pt-3 pb-3 text-light'>
        <Main />
      </main>
    </div>
  );
}

export default App;
