import { useState, useEffect } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { getTransactionTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import { retrieveCategories, retrieveTransactions } from './data'
import Table from './table'
import './css/main.css'

const Transactions = (props) => {
    const [state, setState] = useState({
        categoryDict: {},
        transactionList: [],
        originalTransactions: [],
        vendorCategoryChanges: {},
        disableSave: true,
        disableCategorize: false
    });

    useEffect(() => {
        getData()
    }, []);

    const getData = async () => {
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

        const copyList = []
        // Create copy of transactionList
        for (var i=0; i<transactionList.length; i++){
            const transCopy = {...transactionList[i]}
            copyList.push(transCopy);
        }

        setState({...state,
            categoryDict: categoryDict,
            transactionList: transactionList,
            originalTransactions: copyList,
            disableSave: true,
            disableCategorize: false
        });
    }

    const editTransaction = (row) => {
        // Make copy of transactionList
        const updatedTransactions = [...state.transactionList];

        // Find index to update
        const rowIndex = updatedTransactions.findIndex( e => e.id === row.id);

        // Keep track of change
        const originalRow = state.originalTransactions[rowIndex];
        const changes = {...state.vendorCategoryChanges};

        changes[row["id"]] = [originalRow["vendorId"], originalRow["categoryId"], row["vendorId"], row["categoryId"]]
        updatedTransactions[rowIndex] = row

        setState({...state,
            transactionList: updatedTransactions,
            vendorCategoryChanges: changes,
            disableSave: false,
            disableCategorize:true
        });
    }

    const categorize = () => {
        const url = SERVER + "api/categorize";

        const formData = new FormData();
        formData.append("transactionList", JSON.stringify(state.transactionList));

        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((transactionList) => {
                    setState({...state, transactionList: transactionList, disableSave: true, disableCategorize: true});
                });
            }
        })
    }

    const saveChanges = () => {
        const url = SERVER + "api/transactions";
        const formData = new FormData();
        formData.append("transactions", JSON.stringify(state.transactionList));
        formData.append("changes", JSON.stringify(state.vendorCategoryChanges));

        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                setState({...state, disableSave: true, disableCategorize: false});
            }
        })
    }

    return (
        <Container fluid>
            <div style={{margin: "3%"}}>
                <Table dataList={state.transactionList}
                    columns={ getTransactionTableColumns(state.categoryDict) }
                    changeStateData={ editTransaction } />
            </div>
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", margin:"5%"}}>
                <Button variant="outline-dark center-block"
                    onClick={()=>categorize()}
                    disabled={ state.disableCategorize }>
                    Categorize
                </Button>
                <Button variant="outline-dark center-block"
                    onClick={()=>saveChanges()}
                    disabled={ state.disableSave }>
                    Save Changes
                </Button>
            </div>
        </Container>
    )
}

export default Transactions