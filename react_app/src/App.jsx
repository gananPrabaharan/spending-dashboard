import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import Navigation from './navigation';
import Transactions from './transactions'
import React from 'react'
// import Insights from './insights'

const App = () => {
    return (
        <div id="spendingTool">
            <BrowserRouter>
                <Navigation/>
                <Switch>
                    <Redirect exact from='/' to='transactions'/>
                    <Route exact path='/transactions' component={(props) => <Transactions />}/>
                    <Route exact path='/insights' component={(props) => <Transactions />}/>
                </Switch>
            </BrowserRouter>
        </div>
    )
}

export default App