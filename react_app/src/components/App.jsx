import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import Navigation from './navigation';
import Import from './import'
import Budgets from './budgets'
import Transaction from './transactions'
import React from 'react'
import Insights from './insights'
import Login from './login'
import SignUp from './signup'
import { AuthProvider } from "../contexts/AuthContext"

const App = () => {
    return (
        <div id="spendingTool">
            <BrowserRouter>
                <Navigation/>
                <AuthProvider>
                    <Switch>
                        <Redirect exact from='/' to='login'/>
                        <Route exact path='/login' component={(props) => <Login />}/>
                        <Route exact path='/signup' component={(props) => <SignUp />}/>
                        <Route exact path='/import' component={(props) => <Import />}/>
                        <Route exact path='/budgets' component={(props) => <Budgets />}/>
                        <Route exact path='/transactions' component={(props) => <Transaction />}/>
                        <Route exact path='/insights' component={(props) => <Insights />}/>
                    </Switch>
                </AuthProvider>
            </BrowserRouter>
        </div>
    )
}

export default App