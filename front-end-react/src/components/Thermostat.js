import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'
import axios from 'axios';


class Thermostat extends Component {
    constructor(props) {
        super(props)
        this.state = {
            dataLoaded: false,
            thermostat: null,
            errMessage: ''
        }
        this.setTemperature = this.setTemperature.bind(this);
    }

    CancelToken = axios.CancelToken;
    source = this.CancelToken.source();
    abortController = new AbortController();

    temperatureOptions = [18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0];

    componentDidMount() {
        this.updateThermostat()
    }

    updateThermostat() {
        try {
            axios.get(`http://localhost:8000/apps/thermostat/${this.props.match.params.identifier}`, { withCredentials: true, cancelToken: this.source.token })
                .then(response => {
                    this.setState({
                        thermostat: response.data.thermostat,
                        remoteSensors: response.data.thermostat.data.remoteSensors,
                        dataLoaded: true
                    })
                })
                .catch(error => {
                    console.log(error)
                    this.setState({ errMessage: 'Error retreiving data.' })
                });
        }
        catch (error) {
            if (axios.isCancel(error)) {
                console.log("Request canceled", error.message);
                throw new Error("Cancelled");
            }
        }

    }

    render() {
        const { dataLoaded, thermostat, errMessage } = this.state
        return (
            <React.Fragment>
                {dataLoaded &&
                    <div className='row'>
                        <div className='col-lg-6 mb-4'>
                            <div className='card bg-dark'>
                                <div className='card-header'>
                                    <h1 className='text-center'>{thermostat.data.name}</h1>
                                </div>
                                <div className='card-body'>
                                    <img src='/favicon.ico' className="img-fluid mx-auto d-block" style={{ height: '40px' }} alt="" />
                                    <h1 className='card-title text-center'>
                                        {this.ecobeeTempToDegrees(thermostat.data.runtime.actualTemperature)} C
                                    </h1>
                                    <h5 className='text-center'>HVAC Mode: {this.capitalize(thermostat.data.settings.hvacMode)}</h5>

                                    <div className="input-group">
                                        <div className="input-group-prepend">
                                            <label className="input-group-text" htmlFor="temperature">
                                                {this.capitalize(this.currentClimateRef())}
                                            </label>
                                        </div>
                                        <select defaultValue={this.currentClimateRefTemp()} onChange={this.setTemperature} className='custom-select' style={{ textAlignLast: 'center' }}>
                                            {
                                                this.temperatureOptions.map((option, index) => <option key={index} value={option}>{option}</option>)
                                            }
                                        </select>
                                        <div className='input-group-append'>
                                            <span className="input-group-text" id="basic-addon2">
                                                <div>
                                                    {thermostat.data.events.length ? (
                                                        `C until ${thermostat.data.events[0].endDate} ${thermostat.data.events[0].endTime}`) :
                                                        'C until next transition.'
                                                    }
                                                </div>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div >
                        <div className='col-lg-6 mb-4'>
                            <div className='card bg-dark'>
                                <div className='card-header'>
                                    <h1 className='text-center'>Thermostat Setting</h1>
                                </div>
                                <div className='card-body'>
                                    <div className='btn-group w-100 mb-3'>
                                        <button value='heat' className={`btn btn-outline-light ${this.isHeatOn() && "active"}`} style={{ width: '50%' }}>
                                            Heat</button>
                                        <button value='off' className={`btn btn-outline-light ${!this.isHeatOn() && "active"}`} style={{ width: '50%' }}>
                                            Off</button>
                                    </div>
                                    <div className='btn-group w-100 mb-3'>
                                        <button className={`btn btn-outline-light ${this.isOnClimateHold() && 'active'} ${!thermostat.data.events.length && 'disabled'}`} style={{ width: '25%' }}>
                                            {this.isOnClimateHold() ? ('Hold') : ('Reg')}
                                        </button>
                                        {
                                            this.state.thermostat.data.program.climates.map((climate, index) =>
                                                <button key={index} className={`btn btn-outline-light ${this.currentClimateRef() === climate.climateRef && 'active'}`} style={{ width: '25%' }}>{this.capitalize(climate.climateRef)}</button>
                                            )
                                        }
                                    </div>
                                    <button type='submit' className='btn btn-outline-light btn-block'> Resume Program</button>
                                </div>
                            </div>
                        </div>
                        {
                            this.state.remoteSensors.map((sensor, index) => (
                                <div key={index} className='col-md-6 col-lg-3 mb-4'>
                                    <div key={index} className="card bg-dark" style={{ height: '230px' }}>
                                        <h5 className="card-header">{sensor.name}</h5>
                                        <div className="card-body">
                                            <div className="card-text">{this.getTemperature(sensor) ? (
                                                <React.Fragment>
                                                    Type: {sensor.type === 'ecobee3_remote_sensor' ? "remote sensor" : "thermostat"}<br />
                                                    Temperature: <span className="badge badge-success">{this.getTemperature(sensor)}</span><br />

                                                    Occupancy: <span className={"badge " + (this.getSensorOccupancy(sensor) ? 'badge-success' : 'badge-danger')}>Status</span>
                                                </React.Fragment>
                                            ) : `Thermostat has lost connection with sensor.${sensor.temperature}`}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        }

                        <div className='col-lg-12'>
                            <div className="form-group">
                                <h3><label htmlFor="message">Thermostat Messaging</label></h3>
                                <textarea className="form-control" rows="6"></textarea>
                            </div>
                            <button type='submit' className='btn btn-outline-light btn-block mb-3'>Send Message</button>
                        </div>
                    </div >
                }
            </React.Fragment >
        );
    }

    ecobeeTempToDegrees(temperature) {
        temperature = (temperature / 10 - 32) * 5 / 9
        temperature = Math.round(temperature * 10) / 10
        return temperature
    }

    capitalize(str) {
        str = str.split('');
        let result = str[0].toUpperCase() + str.slice(1).join('');
        return result
    }

    currentClimateRef() {
        let currentClimateRef;
        if (this.state.thermostat.data.events.length) {
            if (this.state.thermostat.data.events[0].holdClimateRef === '') {
                currentClimateRef = 'hold'
            }
            else {
                currentClimateRef = this.state.thermostat.data.events[0].holdClimateRef
            }
        }
        else {
            currentClimateRef = this.state.thermostat.data.program.currentClimateRef
        }
        return currentClimateRef
    }

    currentClimateRefTemp() {
        let temperature;
        let climate;
        if (this.state.thermostat.data.events.length) {
            temperature = this.state.thermostat.data.events[0].heatHoldTemp
        }
        else {
            for (climate of this.state.thermostat.data.program.climates) {
                if (this.currentClimateRef() === climate.climateRef) {
                    temperature = climate.heatTemp
                }
            }
        }
        return this.ecobeeTempToDegrees(temperature)
    }

    setTemperature(event) {
        let key = this.state.thermostat.api_key
        let identifier = this.state.thermostat.data.identifier
        let temperature = event.target.value
        let data = {
            key: key,
            identifier: identifier,
            temperature: temperature
        }
        try {
            axios.post(`http://localhost:8000/apps/setTemperature`, data, { withCredentials: true, cancelToken: this.source.token })
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                    this.setState({ errMessage: 'Error retreiving data.' })
                });
        }
        catch (error) {
            if (axios.isCancel(error)) {
                console.log("Request canceled", error.message);
                throw new Error("Cancelled");
            }
        }
        this.updateThermostat()
    }

    getTemperature(sensor) {
        let capabilities = sensor.capability
        for (let i = 0; i < capabilities.length; i++) {
            let capability = capabilities[i]
            if (capability.type === 'temperature') {
                return this.ecobeeTempToDegrees(capability.value)
            }
        }
    }

    getSensorOccupancy(sensor) {
        let capabilities = sensor.capability
        for (let i = 0; i < capabilities.length; i++) {
            let capability = capabilities[i]
            if (capability.type === 'occupancy') {
                return capability.value === 'true'
            }
        }
    }

    isHeatOn() {
        return this.state.thermostat.data.settings.hvacMode === 'heat'

    }

    isOnClimateHold() {
        return this.state.thermostat.data.events.length
    }

}


export default withRouter(Thermostat);