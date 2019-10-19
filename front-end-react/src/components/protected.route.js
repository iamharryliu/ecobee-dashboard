import React from 'react'
import Auth from './Auth'

import { Route, Redirect } from 'react-router-dom'

export const ProtectedRoute = ({ component: Component, ...rest }) => {
    return (
        <Route
            {...rest}
            render={props => {
                if (Auth.isAuthenticated()) {
                    return <Component {...props} />;
                }
                else {
                    return <Redirect to={
                        {
                            pathname: "/",
                            state: {
                                from: props.location
                            }
                        }
                    } />
                }
            }}
        />
    )
}