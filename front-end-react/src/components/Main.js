import React, { Component } from 'react';
import { withRouter, Link } from 'react-router-dom'

class Main extends Component {

    constructor(props) {
        super(props)
        this.state = {}
    }

    render() {
        const { isLoggedIn } = this.props
        return (
            <div className='jumbotron mt-3 mb-3'>
                <div className='text-dark'>
                    <h1 className='display-4'>Ecobee Dash</h1>
                    <p className='lead'>Have control over your thermostat.</p>
                    <hr className='my-4' />
                    <p>Minimalist Ecobee web app designed to have full control over your Ecobee app.</p>
                </div>
                {
                    !isLoggedIn ?
                        <p className='lead text-light'>
                            <Link to='/login' className='btn btn-primary btn-lg'>Login</Link>
                            <Link to='/register' className='btn btn-primary btn-lg'>Register</Link>
                        </p>
                        :
                        <p className='lead text-light'>
                            <Link to='/thermostats' className='btn btn-primary btn-lg'>View Thermostats</Link>
                            <Link to='/apps' className='btn btn-primary btn-lg'>View Apps</Link>
                        </p>
                }
            </div>
        )
    }

}

export default withRouter(Main)

