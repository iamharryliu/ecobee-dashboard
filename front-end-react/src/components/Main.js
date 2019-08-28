import React from 'react'
import auth from './auth';
import { Link } from 'react-router-dom'

const Main = () => {
    return (
        < div className='jumbotron mt-3 mb-3' >
            <div className='text-dark'>
                <h1 className='display-4'>Ecobee Dash</h1>
                <p className='lead'>Have control over your thermostat.</p>
                <hr className='my-4' />
                <p>Minimalist Ecobee web app designed to have full control over your Ecobee app.</p>
            </div>
            {!auth.isAuthenticated() ?
                <p className='lead text-light'>
                    <Link to='/login' className='btn btn-primary btn-lg'>Login</Link>
                    <Link to='/register' className='btn btn-primary btn-lg'>Register</Link>
                </p>
                :
                <p className='lead text-light'>
                    <Link to='/apps' className='btn btn-primary btn-lg'>View Apps</Link>
                    <Link to='/thermostats' className='btn btn-primary btn-lg'>Thermostats</Link>
                </p>
            }
        </div >
    )
}

export default Main

