import React, { Component } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { transactionTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import Table from './table'


class Transactions extends Component {
    constructor(props){
        super(props)

        this.state = {
            file: null,
            transactions: []
        }
    }

    async fileHandler(e) {
        await this.setState({fileList: e.target.files})
        const url = SERVER + "api/upload";
        const formData = new FormData();



        const options = getRequestOptions()
        fetch(url, options)
            .then((response) => {
                if (response.status === 200){
                }
            })
    }

    onSubmit(){
        console.info("onSubmit")
    }

    render(){
        return (
            <Container fluid>
                <div style={{margin: "3%"}}>
                    <div style={{ paddingBottom: "16px" }}>
                        <div>
                            <input type="file" onChange={this.fileHandler} style={{width:"250px"}}/>
                        </div>
                    </div>
                    <Table dataList={this.state.transactions} columns={transactionTableColumns} />
                </div>
            </Container>
        )
    }
}

export default Transactions