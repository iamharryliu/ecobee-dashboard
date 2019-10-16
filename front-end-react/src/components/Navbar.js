import React, { Component } from 'react';
import { withRouter, Link } from 'react-router-dom'

class Navbar extends Component {
    constructor(props) {
        super(props)
        this.logout = this.logout.bind(this)
        this.state = {}
    }

    logout() {
        this.props.logout(() => this.props.history.push('/'))
    }

    render() {
        const { isLoggedIn } = this.props
        return (
            <nav className="navbar navbar-expand-md navbar-dark fixed-top" >
                <div className='container'>
                    <Link to='/' className="navbar-brand">
                        <img src='/favicon.ico' width="50" height="50" className="d-inline-block align-top" alt="" />
                    </Link>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mr-auto">
                            {isLoggedIn &&
                                <div className="navbar-nav">
                                    <li className="nav-item">
                                        <Link to='/thermostats' className="nav-link">Thermostats</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link to='/apps' className="nav-link">Apps</Link>
                                    </li>
                                </div>
                            }
                        </ul>
                        {!isLoggedIn &&
                            <div>
                                <ul className="navbar-nav">
                                    <li className="nav-item">
                                        <Link to='login' className="nav-link">Login</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link to='/register' className="nav-link">Register</Link>
                                    </li>
                                </ul>
                            </div>
                        }
                        {isLoggedIn &&
                            <ul className="navbar-nav">
                                <li className="nav-item">
                                    <div onClick={this.logout} className="nav-link">Logout</div>
                                </li>
                            </ul >
                        }
                    </div>
                </div>
            </nav >
        )
    }
}

export default withRouter(Navbar)