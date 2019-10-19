import axios from 'axios';

class Auth {

    constructor() {
        this.authenticated = false;
    }

    loginStatus() {
        return axios.get('http://localhost:8000/users/loginStatus', { withCredentials: true })
            .then(response => {
                this.authenticated = response.data.status
                return response.data.status
            })
    }

    setStatus(status){
        this.authenticated = status
    }

    isAuthenticated() {
        return this.authenticated
    }

}

export default new Auth()