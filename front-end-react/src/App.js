import React from 'react';
// import logo from './logo.svg';
import './App.css';
import Main from './components/Main.js';
import Navbar from './components/Navbar.js';
import Apps from './components/Apps.js';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className='container pt-3 pb-3 text-light'>
          <Switch>
            <Route path='/' exact component={Main} />
            <Route path='/apps' component={Apps} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;
