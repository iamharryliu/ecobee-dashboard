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

    login(cb) {
        this.authenticated = true;
        cb();
    }

    logout(cb) {
        this.authenticated = false;
        axios.post('http://localhost:5000/logoutUser', null, { withCredentials: true })
            .then(response => {
                if (response.data.success) {
                    console.log("You have successfully logged out.")
                }
            })
            .catch(error => {
                console.log(error)
            });
        cb();
    }

    isAuthenticated() {
        return this.authenticated
    }

}

export default new Auth()