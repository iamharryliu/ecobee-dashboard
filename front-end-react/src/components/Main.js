import React from 'react'

const Main = () => {
    return (
        <div className='jumbotron mt-3 mb-3'>
            <div className='text-dark'>
                <h1 className='display-4'>Ecobee Dash</h1>
                <p className='lead'>Have control over your thermostat.</p>
                <hr className='my-4' />
                <p>Minimalist Ecobee web app designed to have full control over your Ecobee app.</p>
            </div>
            <p className='lead text-light'>
                <a href='/login' className='btn btn-primary btn-lg'>Login</a>
                <a href='/register' className='btn btn-primary btn-lg'>Register</a>
                <a href='/apps' className='btn btn-primary btn-lg'>View Apps</a>
                <a href='/thermostats' className='btn btn-primary btn-lg'>Thermostats</a>
            </p>
        </div>
    )
}
export default Main

