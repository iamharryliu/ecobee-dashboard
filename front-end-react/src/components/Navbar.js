import React from 'react'

const Navbar = () => {
    return (
        <nav class="navbar navbar-expand-md navbar-dark fixed-top">
            <div class='container'>
                <a class="navbar-brand">
                    <img src='favicon.ico' width="50" height="50" class="d-inline-block align-top" alt="" />
                </a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item">
                            <a class="nav-link">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">Your Apps</a>
                        </li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">Register</a>
                        </li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link">Logout</a>
                        </li>
                    </ul >
                </div >
            </div >
        </nav >
    )
}
export default Navbar