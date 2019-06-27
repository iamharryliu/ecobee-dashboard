import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class APIService {

    constructor() { }
    getAPIS() {
        return [
            {'name':'app1'},
            {'name':'app2'}
            ];
    }

    deleteAPI(){
        console.log('delete')
    }

}

