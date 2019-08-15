import React from 'react'

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-md navbar-dark fixed-top">
            <div className='container'>
                <a href='/' className="navbar-brand">
                    <img src='favicon.ico' width="50" height="50" className="d-inline-block align-top" alt="" />
                </a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <a href='/' className="nav-link">Home</a>
                        </li>
                        <li className="nav-item">
                            <a href='/apps' className="nav-link">Your Apps</a>
                        </li>
                    </ul>
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <a href='/login' className="nav-link">Login</a>
                        </li>
                        <li className="nav-item">
                            <a href='/register' className="nav-link">Register</a>
                        </li>
                    </ul>
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <a href='logout' className="nav-link">Logout</a>
                        </li>
                    </ul >
                </div >
            </div >
        </nav >
    )
}
export default Navbar