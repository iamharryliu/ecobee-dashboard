import React from 'react';
// import logo from './logo.svg';
import './App.css';
import Main from './components/Main.js';
import Navbar from './components/Navbar.js';
import Register from './components/Register'
import Login from './components/Login.js'
import Apps from './components/Apps.js';
import Thermostats from './components/Thermostats.js';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className='container pt-3 pb-3 text-light'>
          <Switch>
            <Route path='/' exact component={Main} />
            <Route path='/register' component={Register} />
            <Route path='/login' component={Login} />
            <Route path='/apps' exact component={Apps} />
            <Route path='/thermostats' component={Thermostats} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;
