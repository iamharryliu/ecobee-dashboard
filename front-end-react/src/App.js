import React, { Component } from 'react';
import './App.css';
import Main from './components/Main';
import Navbar from './components/Navbar';
import Register from './components/Register'
import Login from './components/Login'
import Apps from './components/Apps';
import Thermostats from './components/Thermostats';
import { BrowserRouter as Router, Switch, Route, withRouter } from 'react-router-dom';
import { ProtectedRoute } from './components/protected.route'
import axios from 'axios';

import auth from './components/auth'

class App extends Component {

  constructor(props) {
    super(props)
    this.login = this.login.bind(this)
    this.logout = this.logout.bind(this)
    this.state = {
      isLoggedIn: false,
      dataLoaded: false
    }
  }

  componentDidMount() {
    auth.checkLoginStatus().then(response => {
      this.setState({
        isLoggedIn: response,
        dataLoaded: true
      });
    })
  }

  componentDidUpdate(prevState) {
    if (this.state.isLoggedIn !== prevState.isLoggedIn) {
      console.log('log')
    }
  }

  login(data, cb) {
    axios.post('http://localhost:5000/loginUser', data, { withCredentials: true })
      .then(response => {
        if (response.data.success) {
          console.log('You have successfully logged in.')
          this.setState({ isLoggedIn: true })
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
    axios.post('http://localhost:5000/logoutUser', null, { withCredentials: true })
      .then(response => {
        if (response.data.success) {
          console.log("You have successfully logged out.")
          this.setState({ isLoggedIn: false })
          cb()
        }
      })
      .catch(error => {
        console.log(error)
      });
  }

  render() {
    const { dataLoaded, isLoggedIn } = this.state
    return (
      <Router>
        {dataLoaded &&
          <div className="App">
            <Navbar isLoggedIn={isLoggedIn} logout={this.logout} />
            <main className='container pt-3 pb-3 text-light'>
              <Switch>
                <Route exact path='/' component={() => <Main isLoggedIn={isLoggedIn} />} />
                <Route exact path='/register' component={Register} />
                <Route exact path='/login' component={() => <Login login={this.login} />} />
                <ProtectedRoute exact path='/apps' component={Apps} />
                <ProtectedRoute exact path='/thermostats' component={Thermostats} />
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
