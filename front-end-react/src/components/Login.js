import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

class Login extends Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
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

    handleSubmit = event => {
        event.preventDefault()
        this.props.login(this.state, () =>
            this.props.history.push('/thermostats'))
    }

    render() {
        return (
            <div>
                <h1>Login</h1>
                <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email address</label>
                        <input type="email" className="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" value={this.state.username} onChange={this.changeEmailEventHandler} />
                        <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" className="form-control" id="password" placeholder="Password" value={this.state.password} onChange={this.changePasswordEventHandler} />
                    </div>
                    <div className="form-check">
                        <input type="checkbox" className="form-check-input" id="rememberMe" checked={this.state.rememberMe} onChange={this.changeRememberMeEventHandler} />
                        <label className="form-check-label" htmlFor="rememberMe">Remember Me</label>
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
            </div >
        )
    };
}

export default withRouter(Login);
