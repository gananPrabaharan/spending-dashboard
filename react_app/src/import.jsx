import React, { Component } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { getTransactionTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import { retrieveCategories } from './data'
import Table from './table'


class Import extends Component {
    constructor(props){
        super(props)

        this.state = {
            file: null,
            categoryDict: {},
            transactions: [],
            changesMade: false
        }
    }

    componentDidMount(){
        retrieveCategories().then((result) => {
            const categoryDict = result.data;
            this.setState({categoryDict: categoryDict});
        });
    }

    fileHandler = async (e) => {
        await this.setState({fileList: e.target.files})
        const url = SERVER + "api/parseFile";
        const formData = new FormData();
        formData.append("fileInput", this.state.fileList[0]);

        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((transactionData) => {
                    this.setState({transactions: transactionData, changesMade: true});
                })
            }
        })
    }

    editTransaction = (row) => {
        // Make copy of transactionList
        const updatedTransactions = [...this.state.transactions];

        // Find index to update
        const rowIndex = updatedTransactions.findIndex( e => e.id === row.id);
        updatedTransactions[rowIndex] = row
        this.setState({transactions: updatedTransactions, changesMade: true});
    }

    saveChanges = () => {
        this.setState({changesMade: false});
        const url = SERVER + "api/import";
        const formData = new FormData();
        formData.append("transactions", JSON.stringify(this.state.transactions));

        const options = getRequestOptions("POST", formData)
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((transactionData) => {
                    this.setState({transactions: transactionData, changesMade: false});
                })
            }
        })
    }

    render(){
        return (
            <Container fluid>
                <div style={{margin: "3%"}}>
                    <div style={{ paddingBottom: "16px" }}>
                        <div>
                            <input type="file" onChange={this.fileHandler} style={{width:"250px"}} />
                        </div>
                    </div>
                    <Table dataList={this.state.transactions}
                        columns={ getTransactionTableColumns(this.state.categoryDict) }
                        changeStateData={ this.editTransaction } />
                </div>
                <div style={{ display: "flex", justifyContent: "center", alignItems: "center", margin:"5%"}}>
                    <Button variant="outline-dark center-block"
                            onClick={()=>this.saveChanges()}
                            disabled={ !this.state.changesMade }>
                        Import
                    </Button>
                </div>
            </Container>
        )
    }
}

export default Import