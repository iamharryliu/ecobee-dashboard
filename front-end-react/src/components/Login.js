import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

class Login extends Component {
    constructor(props) {
        super(props)
        this.loginUser = this.loginUser.bind(this)
        this.state = {
            email: '',
            password: '',
            remember: false
        }
    }

    changeEmailEventHandler = (event) => {
        this.setState({ email: event.target.value })
    }

    changePasswordEventHandler = (event) => {
        this.setState({ password: event.target.value })
    }

    changeRememberMeEventHandler = (event) => {
        this.setState({ remember: event.target.checked });
    }

    loginUser = event => {
        event.preventDefault()
        this.props.login(this.state, () =>
            this.props.history.push('/'))
    }

    render() {
        return (
            <React.Fragment>
                <h1>Login</h1>
                <form onSubmit={this.loginUser}>
                    <div className="form-group">
                        <label htmlFor="email">Email address</label>
                        <input type="email" id="email" className="form-control" placeholder="Enter email" autoComplete="off" value={this.state.username} onChange={this.changeEmailEventHandler} />
                        <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" id="password" className="form-control" placeholder="Password" autoComplete="off" value={this.state.password} onChange={this.changePasswordEventHandler} />
                    </div>
                    <div className="form-check">
                        <input type="checkbox" id="rememberMe" className="form-check-input" checked={this.state.rememberMe} onChange={this.changeRememberMeEventHandler} />
                        <label className="form-check-label" htmlFor="rememberMe">Remember Me</label>
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
            </React.Fragment>
        )
    };
}

export default withRouter(Login);
