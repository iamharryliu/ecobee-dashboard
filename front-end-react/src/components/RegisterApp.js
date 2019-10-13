import React, { Component } from 'react';
import axios from 'axios';

class RegisterApp extends Component {

    onMove = () => {
        console.log(this.testVarible);
    }

    constructor(props) {
        super(props)
        this.state = {
            key: '',
            name: '',
            // authorizationCode: '',
        }
    }

    changeKeyEventHandler = event => {
        this.setState({ key: event.target.value })
    }

    changeNameEventHandler = event => {
        this.setState({ name: event.target.value })
        console.log(this.state.name)
    }

    authorizeApp = event => {
        event.preventDefault()
        axios.get(`http://localhost:8000/apps/authorize/${this.state.key}`, { withCredentials: true })
            .then(response => {
                if (response.data.success) {
                    console.log('Successfully authorized app.')
                    this.setState({
                        pin: response.data.data.pin,
                        authorizationCode: response.data.data.authorizationCode
                    })
                }
            })
            .catch(error => {
                console.log(error)
            })
    }

    registerApp = event => {
        event.preventDefault()
        // axios.post('http://localhost:8000/RegisterApp', this.state, { withCredentials: true })
        //     .then(response => {
        //         if (response.data.success) {
        //             console.log('User successfully registered.')
        //             this.props.history.push('/login')
        //         }
        //     })
        //     .catch(error => {
        //         console.log(error)
        //     })
    }

    render() {
        return (
            <React.Fragment>
                <h1>Register App</h1>
                <h4>Step 1: <a href="https://www.ecobee.com/home/ecobeeLogin.jsp" target="_blank" rel="noopener noreferrer">Login to Ecobee</a></h4>
                <h4>Step 2: Navigate: Account Menu > Developer</h4>
                <h4>Step 3: Create New App with Ecobee Pin Authentication</h4>
                <h4>Step 4: Enter the API Key provided from the App below and click Authorize App</h4>
                <form className="mt-3" onSubmit={this.authorizeApp}>
                    <div className='row'>
                        <div className='col-12 col-md-6'>
                            <div className="form-group row">
                                <label htmlFor="key" className="col-12 col-md-4 col-form-label">API Key</label>
                                <div className="col-12 col-md-8">
                                    <div>
                                        <input type="text" name='key' id='key' className="form-control" placeholder="Enter API Key" /*autoComplete="off"*/ value={this.state.key} onChange={this.changeKeyEventHandler} />
                                        {/* <small className="text-danger">Key is required.</small>
                                        <small className="text-danger">Key must be {this.props.keyLength} characters long.</small> */}
                                    </div>
                                </div>
                            </div>
                            <input type="hidden" name="authorizationCode" />
                        </div>
                    </div >
                    <button type='submit' className="btn btn-primary mb-2" data-toggle="modal" data-target="#exampleModal">Authorize App</button >
                </form >

                <div className="modal fade text-dark" id="exampleModal" tabIndex="-1" role="dialog" aria-labelledby="exampleModalLabel"
                    aria-hidden="true">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title" id="exampleModalLabel">Register App Form</h5>
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div className="modal-body">
                                <h5>Instructions</h5>
                                <p>
                                    From the Ecobee Page <br />
                                    Navigate: Account Menu > My Apps <br />
                                    Click Add Application and use the pin below to validate the application.
                                    </p>
                                <h5>Pin: {this.state.pin}</h5>
                                <p>
                                    Finally, enter a name for your App that you would like to refer to it as. For example, if it is the
                                    App
                                    for your home thermostat you may put 'Home' as the name or even your address.
                </p>
                                <form id='registerForm'>
                                    <div className="form-group">
                                        <label htmlFor="name" className="col-form-label">App Name:</label>
                                        <input type="text" id="name" className="form-control" placeholder="Enter App Name" autoComplete="off" value={this.state.name} onChange={this.changeNameEventHandler} />
                                        {/* <div>
                                            <small className="text-danger">Name is required.</small>
                                            <small className="text-danger" >name must be at least
                            nameminlength characters
                                long.</small>
                                        </div> */}
                                        <input type="hidden" />
                                        <input type="hidden" />
                                    </div>
                                </form>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                                <button type="submit" className="btn btn-primary" form='registerForm'>Register
                    App</button>
                            </div>
                        </div>
                    </div>
                </div >
            </React.Fragment >

        );
    }
}

export default RegisterApp;