import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import axios from 'axios';


class Thermostats extends Component {
    constructor(props) {
        super(props)
        this.state = {
            thermostats: [],
            errMessage: ''
        }
    }

    componentDidMount() {
        axios.get('http://localhost:5000/getUserThermostats', { withCredentials: true })
            .then(response => {
                this.setState({ thermostats: response.data })
            })
            .catch(error => {
                console.log(error)
                this.setState({ errMessage: 'Error retreiving data.' })
            });
    }

    render() {
        const { thermostats, errMessage } = this.state
        return (
            <div>
                <div className='row'>
                    <h1 className='col-12'> Thermostats</h1 >
                    {
                        errMessage ? <div className='col-12'>{errMessage}</div> : null
                    }
                    {
                        thermostats.length ?
                            thermostats.map(thermostat =>
                                <div className='col-12 mt-3 mb-3 app'>
                                    <div className='card bg-dark'>
                                        <div className='card-body'>
                                            <h2 className='d-inline'>{thermostat.data.name}</h2>
                                            <div className='float-right'>
                                                <Link to='/' className='btn btn-info'>View</Link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) :
                            <div className='col-12 mt-3 mb-3'>
                                You currently have no thermostats registered with this account.
                        </div>
                    }
                </div>
            </div>
        );
    }
}

export default Thermostats;