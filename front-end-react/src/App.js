import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Main from './components/Main';
import Navbar from './components/Navbar';
import Register from './components/Register'
import Login from './components/Login'
import Apps from './components/Apps';
import Thermostats from './components/Thermostats';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ProtectedRoute } from './components/protected.route'

class App extends Component {

  render() {
    return (
      <Router>
        <div className="App">
          <Navbar />
          <main className='container pt-3 pb-3 text-light'>
            <Switch>
              <Route exact path='/' component={Main} />
              <Route exact path='/register' component={Register} />
              <Route exact path='/login' component={Login} />
              <ProtectedRoute exact path='/apps' component={Apps} />
              <ProtectedRoute exact path='/thermostats' component={Thermostats} />
              <Route path='*' component={() => '404 Page'} />
            </Switch>
          </main>
        </div>
      </Router >
    );
  }
}

export default App;
