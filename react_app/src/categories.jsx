import React, { Component } from 'react'
import { Container, Row, Col, Button, Form } from 'react-bootstrap'
import { getCategoriesTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import Table from './table'


class Categories extends Component {
    constructor(props) {
        super(props)
        this.state = {
            categoryList: [],
            categoryToAdd: ""
        }
    }

    componentDidMount(){
        const url = SERVER + "api/categories";
        const options = getRequestOptions("GET");

        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((categoryList) => {
                    this.setState({categoryList: categoryList});
                });
            }
        });
    }

    addCategory(){
        const url = SERVER + "api/categories";
        const categoryToAdd = this.state.categoryToAdd;
        const formData = new FormData();
        formData.append("categoryToAdd", JSON.stringify(categoryToAdd))

        const options = getRequestOptions("POST", formData);

        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((categoryList) => {
                    this.setState({categoryList: categoryList, categoryToAdd: ""});
                });
            }
        });
    }

    deleteCategory = (category) => {
        const deleteId = category.id
        const catToDelete = this.state.categoryList.find(c => c.id === deleteId);
        if (catToDelete != null){
            const url = SERVER + "api/categories";
            const formData = new FormData();
            formData.append("categoryId", JSON.stringify(deleteId));

            const options = getRequestOptions("DELETE", formData);
            fetch(url, options).then((response) => {
                if (response.status === 200){
                    response.json().then((categoryList) => {
                        this.setState({categoryList: categoryList});
                    });
                }
            });
        } else{
            console.error("Missing Row");
        }
    }

    render(){
        return(
            <Container fluid>
                <div style={{margin: "3%", paddingBottom: "20px"}}>
                    <div style={{width: "40%"}}>
                        <Form.Label>Category Name</Form.Label>

                    </div>
                    <div>
                        <div style={{width: "20%", float:"left"}}>
                            <Form.Control type="text"
                                onChange={(e)=>this.setState({categoryToAdd: e.target.value})}
                                value={this.state.categoryToAdd}/>
                        </div>
                        <div style={{width: "10%", float:"left"}}>
                            <Form.Control type="button" value="Add Category" className="outline-dark center-block"
                                onClick={()=>this.addCategory()}
                                disabled={this.state.categoryToAdd == ""}/>
                        </div>
                    </div>
                </div>

                <div style={{margin: "3%"}}>
                    <Table dataList={this.state.categoryList}
                        columns={getCategoriesTableColumns(this.deleteCategory)} />
                </div>
            </Container>
        )
    }
}

export default Categories