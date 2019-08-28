import React, { Component } from 'react';
import axios from 'axios';

class RegisterUser extends Component {
    constructor(props) {
        super(props)
        this.state = {
            username: '',
            email: '',
            password: '',
        }
    }
    changeUsernameEventHandler = (event) => {
        this.setState({ username: event.target.value })
    }
    changeEmailEventHandler = (event) => {
        this.setState({ email: event.target.value })
    }
    changePasswordEventHandler = (event) => {
        this.setState({ password: event.target.value })
    }
    handleSubmit = (event) => {
        event.preventDefault()
        axios.post('http://localhost:5000/registerUser', this.state, { withCredentials: true })
            .then(response => {
                if (response.data.success) {
                    console.log('User successfully registered.')
                    this.props.history.push('/login')
                }
            })
            .catch(error => {
                console.log(error)
            })
    }


    render() {
        return (
            <div>
                <h1>Register User</h1>
                <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input type="text" className="form-control" id="username" aria-describedby="emailHelp" placeholder="Enter username" value={this.state.username} onChange={this.changeUsernameEventHandler} />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email address</label>
                        <input type="email" className="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" value={this.state.email} onChange={this.changeEmailEventHandler} />
                        <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" className="form-control" id="password" value={this.state.password} onChange={this.changePasswordEventHandler} placeholder="Password" />
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
            </div >

        );
    }
}

export default RegisterUser;