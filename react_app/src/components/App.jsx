import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import Navigation from './Navigation';
import PrivateRoute from './PrivateRoute'
import Import from './Import'
import Budgets from './Budgets'
import Transaction from './Transactions'
import React from 'react'
import Insights from './Insights'
import Login from './Login'
import SignUp from './Signup'
import { AuthProvider } from "../contexts/AuthContext"

const App = () => {
    return (
        <div id="spendingTool">
            <BrowserRouter>
                <Navigation/>
                <AuthProvider>
                    <Switch>
                        <Redirect exact from='/' to='transactions'/>
                        <Route exact path='/login' component={(props) => <Login />}/>
                        <Route exact path='/signup' component={(props) => <SignUp />}/>
                        <PrivateRoute exact path='/import' component={(props) => <Import />}/>
                        <PrivateRoute exact path='/budgets' component={(props) => <Budgets />}/>
                        <PrivateRoute exact path='/transactions' component={(props) => <Transaction />}/>
                        <PrivateRoute exact path='/insights' component={(props) => <Insights />}/>
                    </Switch>
                </AuthProvider>
            </BrowserRouter>
        </div>
    )
}

export default App