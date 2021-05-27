import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import Navigation from './navigation';
import Import from './import'
import Categories from './categories'
import Transaction from './transactions'
import React from 'react'
// import Insights from './insights'

const App = () => {
    return (
        <div id="spendingTool">
            <BrowserRouter>
                <Navigation/>
                <Switch>
                    <Redirect exact from='/' to='import'/>
                    <Route exact path='/import' component={(props) => <Import />}/>
                    <Route exact path='/categories' component={(props) => <Categories />}/>
                    <Route exact path='/transactions' component={(props) => <Transaction />}/>
                </Switch>
            </BrowserRouter>
        </div>
    )
}

export default App