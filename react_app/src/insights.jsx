import { useState, useEffect } from 'react'
import { retrieveCategories, retrieveTransactions } from './data'

import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './css/insights.css'

const Insights = (props) => {
    const [dateState, setDateState] = useState({
        startDate: new Date(),
        endDate: new Date()
    });

    const [state, setState] = useState({
        transactionList: [],
        categoryDict: {}
    });

    useEffect(() => {
        initialize();
    }, []);

    const initialize = async () => {
        const catResult = await retrieveCategories();
        const transResult = await retrieveTransactions();

        let categoryDict = {};
        let transactionList = [];
        if (catResult.status === 200){
            categoryDict = catResult.data;
        }
        if (transResult.status === 200){
            transactionList = transResult.data;
        }

        setState({...state,
            categoryDict: categoryDict,
            transactionList: transactionList,
            disableSave: true,
            disableCategorize: false
        });

        const currentDate = new Date();
        const startDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        setDateState({startDate: startDate, endDate: currentDate});
    }

    return (
    <div style={{margin: "3%"}}>
        <DatePicker className='datePicker' selected={dateState.startDate} onChange={date => setDateState({...dateState, startDate: date})}/>
        <DatePicker className='datePicker' selected={dateState.endDate} onChange={date => setDateState({...dateState, endDate: date})}/>
    </div>

    );
}

export default Insights