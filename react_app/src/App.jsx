import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import Navigation from './navigation';
import Import from './import'
import Budgets from './budgets'
import Transaction from './transactions'
import React from 'react'
import Insights from './insights'
import Vendors from './vendors'
import Login from './login'


const App = () => {
    return (
        <div id="spendingTool">
            <BrowserRouter>
                <Navigation/>
                <Switch>
                    <Redirect exact from='/' to='transactions'/>
                    <Route exact path='/login' component={(props) => <Login />}/>
                    <Route exact path='/import' component={(props) => <Import />}/>
                    <Route exact path='/budgets' component={(props) => <Budgets />}/>
                    <Route exact path='/transactions' component={(props) => <Transaction />}/>
                    <Route exact path='/insights' component={(props) => <Insights />}/>
                    <Route exact path='/vendors' component={(props) => <Vendors />}/>
                </Switch>
            </BrowserRouter>
        </div>
    )
}

export default App