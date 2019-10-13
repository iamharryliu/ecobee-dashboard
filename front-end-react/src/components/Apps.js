import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import axios from 'axios';

class Apps extends Component {
    constructor(props) {
        super(props)
        this.state = {
            dataLoaded: false,
            apps: [],
            errMessage: ''
        }
    }

    componentDidMount() {
        axios.get('http://localhost:8000/apps', { withCredentials: true })
            .then(response => {
                this.setState({
                    dataLoaded: true,
                    apps: response.data
                })
            })
            .catch(error => {
                console.log(error)
                this.setState({ errMessage: 'Error retreiving data.' })
            });
    }

    render() {
        const { dataLoaded, apps, errMessage } = this.state
        return (
            <React.Fragment>
                {dataLoaded &&
                    <div className='row'>
                        <h1 className='col-6'>Apps</h1>
                        <div className='col-6'>
                            <Link to='apps/register' className='btn btn-primary btn-lg float-right'>Register App</Link>
                        </div>
                        {
                            errMessage ? <div className='col-12'>{errMessage}</div> : null
                        }
                        {
                            apps.length ?
                                apps.map(app =>
                                    <div key={app.key} className='col-12 mt-3 mb-3 app'>
                                        <div className='card bg-dark'>
                                            <div className='card-body'>
                                                <h2 className='d-inline'>{app.name}</h2>
                                                <div className='float-right'>
                                                    <Link to='thermostats' className='btn btn-info'>View</Link>
                                                    <Link to='blank' className='btn btn-info'>Reauthorize</Link>
                                                    <Link to='blank' className='btn btn-info'>Update App Credentials</Link>
                                                    <button className='btn btn-danger'>Delete</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div >
                                ) :
                                <div className='col-12 mt-3 mb-3'>
                                    You currently have no apps registered with this account.
                        </div>
                        }
                    </div>
                }

            </React.Fragment >

        );
    }
}

export default Apps;
