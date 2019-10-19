import React, { Component } from 'react';
import axios from 'axios';
import './App.css';
import { BrowserRouter as Router, Switch, Route, withRouter } from 'react-router-dom';
import { ProtectedRoute } from './components/protected.route'

import Main from './components/Main';
import Navbar from './components/Navbar';
import RegisterUser from './components/RegisterUser';
import Login from './components/Login';
import Apps from './components/Apps';
import RegisterApp from './components/RegisterApp';
import Thermostats from './components/Thermostats';
import Thermostat from './components/Thermostat';


import Auth from './components/Auth'

class App extends Component {

  constructor(props) {
    super(props)
    this.login = this.login.bind(this)
    this.logout = this.logout.bind(this)
    this.state = {
      dataLoaded: false,
      isLoggedIn: false,
      keyLength: 32
    }
  }

  componentDidMount() {
    Auth.loginStatus().then(response => {
      this.setState({
        isLoggedIn: response,
        dataLoaded: true
      });
    })
  }

  login(data, cb) {
    axios.post('http://localhost:8000/users/login', data, { withCredentials: true })
      .then(response => {
        if (response.data.success) {
          console.log('You have successfully logged in.')
          this.setState({ isLoggedIn: true })
          Auth.setStatus(true)
          cb()
        }
        else {
          alert('Unsuccessful login.')
        }
      })
      .catch(error => {
        console.log(error)
      })
  }

  logout(cb) {
    axios.post('http://localhost:8000/users/logout', null, { withCredentials: true })
      .then(response => {
        if (response.data.success) {
          console.log("You have successfully logged out.")
          this.setState({ isLoggedIn: false })
          Auth.setStatus(false)
          cb()
        }
      })
      .catch(error => {
        console.log(error)
      });
  }

  render() {
    const { dataLoaded, isLoggedIn, keyLength } = this.state
    return (
      <Router>
        {dataLoaded &&
          <div className="App">
            <Navbar isLoggedIn={isLoggedIn} logout={this.logout} />
            <main className='container pt-3 pb-3 text-light'>
              <Switch>
                <Route exact path='/' component={() => <Main isLoggedIn={isLoggedIn} />} />
                <Route exact path='/register' component={RegisterUser} />
                <Route exact path='/login' component={() => <Login login={this.login} />} />
                <ProtectedRoute exact path='/apps' component={Apps} />
                <ProtectedRoute exact path='/apps/register' component={RegisterApp} keyLength={keyLength} />
                <ProtectedRoute exact path='/thermostats' component={Thermostats} />
                <ProtectedRoute exact path='/thermostats/:key/:identifier' component={Thermostat} />
                <Route path='*' component={() => '404 Page'} />
              </Switch>
            </main>
          </div>
        }
      </Router >
    );
  }
}

export default withRouter(App);
