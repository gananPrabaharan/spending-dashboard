import React, { Component, useState, useEffect } from 'react'
import { Container, Button } from 'react-bootstrap'
import { getTransactionTableColumns } from '../utilities/TableColumns'
import { SERVER, getRequestOptions } from '../utilities/Util'
import { retrieveCategories } from '../utilities/Data'
import Table from './Table'
import { useAuth } from "../contexts/AuthContext"


const Import = (props) => {
    const [state, setState] = useState({
        file: null,
        categoryDict: {},
        transactions: [],
        changesMade: false
    });

    const { currentUser } = useAuth();

    useEffect(() => {
        getCategories();
    }, []);

    const getCategories = async () => {
        const idToken = await currentUser.getIdToken();
        retrieveCategories(idToken).then((result) => {
            const categoryDict = result.data;
            console.info(categoryDict)
            setState({...state, categoryDict: categoryDict});
        });
    }

    const fileHandler = async (e) => {
        const fileList = e.target.files;
        await setState({...state, fileList: fileList});
        const url = SERVER + "api/parseFile";
        const formData = new FormData();
        formData.append("fileInput", fileList[0]);

        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((transactionData) => {
                console.info(transactionData);
                    setState({...state, transactions: transactionData, changesMade: true});
                })
            }
        })
    }

    const editTransaction = (row) => {
        // Make copy of transactionList
        const updatedTransactions = [...state.transactions];

        // Find index to update
        const rowIndex = updatedTransactions.findIndex( e => e.id === row.id);
        updatedTransactions[rowIndex] = row
        setState({...state, transactions: updatedTransactions, changesMade: true});
    }

    const saveChanges = async() => {
        setState({...state, changesMade: false});
        const url = SERVER + "api/import";
        const idToken = await currentUser.getIdToken();

        const formData = new FormData();
        formData.append("transactions", JSON.stringify(state.transactions));

        const options = getRequestOptions("POST", formData, idToken)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((transactionData) => {
                    setState({...state, transactions: transactionData, changesMade: false});
                })
            }
        })
    }

    return (
        <Container fluid>
            <div style={{margin: "3%"}}>
                <div style={{ paddingBottom: "16px" }}>
                    <div>
                        <input type="file" onChange={fileHandler} style={{width:"250px"}} />
                    </div>
                </div>
                <Table dataList={state.transactions}
                    columns={ getTransactionTableColumns(state.categoryDict) }
                    changeStateData={ editTransaction } />
            </div>
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", margin:"5%"}}>
                <Button variant="outline-dark center-block"
                    onClick={()=>saveChanges()}
                    disabled={ !state.changesMade }>
                    Import
                </Button>
            </div>
        </Container>
    )
}

export default Import