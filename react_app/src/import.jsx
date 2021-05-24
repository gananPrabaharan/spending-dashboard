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
            categoryList: [],
            transactions: [],
            changesMade: false
        }
    }

    componentDidMount(){
        retrieveCategories().then((result) => {
            const categoryDictList = result.data;
            const catNameList = categoryDictList.map((cat) => { return cat.name } )
            this.setState({categoryList: catNameList});
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

    editTransaction = (transactionData) => {
        this.setState({transactions: transactionData, changesMade: true});
    }

    saveChanges = () => {
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
                        columns={ getTransactionTableColumns(this.state.categoryList) }
                        changeStateData={ this.editTransaction } />
                </div>
                <div style={{ display: "flex", justifyContent: "center", alignItems: "center", margin:"5%"}}>
                    <Button variant="outline-dark center-block"
                            onClick={()=>this.saveChanges()}
                            disabled={ !this.state.changesMade }>
                        Save Changes
                    </Button>
                </div>
            </Container>
        )
    }
}

export default Import