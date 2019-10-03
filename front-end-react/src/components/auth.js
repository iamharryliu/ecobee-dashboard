import axios from 'axios';

class Auth {

    constructor() {
        this.authenticated = false;
    }

    checkLoginStatus() {
        return axios.get('http://localhost:5000/getLoggedInStatus', { withCredentials: true })
            .then(response => {
                this.authenticated = true
                return response.data.success
            })
    }

    isAuthenticated() {
        return this.authenticated
    }

}

export default new Auth()