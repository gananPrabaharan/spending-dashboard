import { useState, useEffect } from 'react'
import { retrieveCategories, retrieveTransactions } from './data'
import BudgetVisualizer from './graphing/budgetVisualizer.jsx'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './css/insights.css'

const Insights = (props) => {
    const [dateState, setDateState] = useState({
        startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1),
        endDate: new Date()
    });

    const [state, setState] = useState({
        transactionList: [],
        categoryDict: {}
    });

    const [chartState, setChartState] = useState({
        chartData: {}
    });

    useEffect(() => {
        initialize();
    }, [dateState]);

    const initialize = async () => {
        // Retrieve categories and transactions from backend
        const catResult = await retrieveCategories();
        const transResult = await retrieveTransactions(dateState.startDate, dateState.endDate);
        
        // Store backend data in state
        let categoryDict = {};
        if (catResult.status === 200){
            categoryDict = catResult.data;
        }
        
        let transactionList = [];
        if (transResult.status === 200){
            transactionList = transResult.data;
        }

        // Store backend data in state
        setState({...state,
            transactionList: transactionList,
            categoryDict: categoryDict
        });
        
    }
    
    return (
        <div style={{margin: "3%"}}>
            <DatePicker className='datePicker' selected={dateState.startDate} onChange={date => setDateState({...dateState, startDate: date})}/>
            <DatePicker className='datePicker' selected={dateState.endDate} onChange={date => setDateState({...dateState, endDate: date})}/>
            <BudgetVisualizer transactions={state.transactionList} categoryDict={state.categoryDict}></BudgetVisualizer>
        </div>
    );
}

export default Insights