import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Button, Form } from 'react-bootstrap'
import { getCategoriesTableColumns } from './tableColumns'
import { SERVER, getRequestOptions } from './util'
import { retrieveCategories } from './data'
import Table from './table'
import './css/main.css'

const Categories = (props) => {
    const [state, setState] = useState({
        categoryList: [],
        categoryToAdd: ""
    });

    useEffect(() => {
        getCategories()
    }, [])

    const getCategories = async () => {
        const catResult = await retrieveCategories();

        let categoryList = [];
        if (catResult.status === 200){
            categoryList = catResult.data;
        }
        const validCategories = categoryList.filter(catDict => catDict["name"].length > 0);
        setState({...state, categoryList: validCategories, changesMade: false});
    }

    const addCategory = () => {
        const url = SERVER + "api/categories";
        const formData = new FormData();
        formData.append("categoryToAdd", JSON.stringify(state.categoryToAdd))
        const options = getRequestOptions("POST", formData);

        fetch(url, options).then((response) => {
            if (response.status === 200){
                getCategories();
            }
        });
    }

    const deleteCategory = (category) => {
        const deleteId = category.id
        const catToDelete = state.categoryList.find(c => c.id === deleteId);
        if (catToDelete != null){
            const url = SERVER + "api/categories";
            const formData = new FormData();
            formData.append("categoryId", JSON.stringify(deleteId));

            const options = getRequestOptions("DELETE", formData);
            fetch(url, options).then((response) => {
                if (response.status === 200){
                    response.json().then((categoryList) => {
                        setState({...state, categoryList: categoryList});
                    });
                }
            });
        } else{
            console.error("Missing Row");
        }
    }

    return(
        <Container fluid>
            <div style={{margin: "3%"}}>
                <div style={{width: "40%"}}>
                    <Form.Label>Category Name</Form.Label>
                </div>
                <div>
                    <div style={{float:"left", width:"300px"}}>
                        <Form.Control type="text"
                            onChange={(e) => setState({...state, categoryToAdd: e.target.value})}
                            value={state.categoryToAdd}/>
                    </div>
                    <div>
                        <Button variant="outline-dark center-block"
                            onClick={() => addCategory()}
                            disabled={state.categoryToAdd == ""}>
                            Add Category
                        </Button>
                    </div>
                </div>
            </div>

            <div style={{margin: "3%"}}>
                <Table dataList={state.categoryList}
                    columns={getCategoriesTableColumns(deleteCategory)} />
            </div>
        </Container>
    )
}

export default Categories