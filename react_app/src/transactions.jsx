import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { getTransactionTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import { retrieveCategories, retrieveTransactions } from './data'
import Table from './table'
import './css/main.css'

const Transactions = (props) => {
    const [state, setState] = useState({
        categoryList: [],
        transactionList: [],
        changesMade: false
    });

    useEffect(() => {
        getData()
    }, []);

    const getData = async () => {
        const catResult = await retrieveCategories();
        const transResult = await retrieveTransactions();

        let catNameList = [];
        let transactionList = [];
        if (catResult.status === 200){
            catNameList = catResult.data.map((cat) => { return cat.name } )
        }
        if (transResult.status === 200){
            transactionList = transResult.data;
        }
        setState({...state, categoryList: catNameList, transactionList: transactionList, changesMade: false});
    }

    const editTransaction = (transactionData) => {
        setState({...state, transactionList: transactionData, changesMade: true});
    }

    const saveChanges = () => {
        const url = SERVER + "api/transactions";
        const formData = new FormData();
        formData.append("transactions", JSON.stringify(state.transactionList));
        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                setState({...state, changesMade: false});
            }
        })
    }

    return (
        <Container fluid>
            <div style={{margin: "3%"}}>
                <Table dataList={state.transactionList}
                    columns={ getTransactionTableColumns(state.categoryList) }
                    changeStateData={ editTransaction } />
            </div>
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", margin:"5%"}}>
                <Button variant="outline-dark center-block"
                    onClick={()=>saveChanges()}
                    disabled={ !state.changesMade }>
                    Save Changes
                </Button>
            </div>
        </Container>
    )
}

export default Transactions