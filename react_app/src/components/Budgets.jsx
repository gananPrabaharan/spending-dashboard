import React, { useState, useEffect } from 'react'

import { Container, Row, Col, Button, Form } from 'react-bootstrap'
import { getCategoriesTableColumns } from './utilities/tableColumns'
import { SERVER, getRequestOptions, validateNumbers } from './util'
import { retrieveCategories } from './utilities/data'
import Table from './table'
import './css/main.css'


const Budgets = (props) => {
    const [state, setState] = useState({
        categoryList: [],
        categoryName: "",
        categoryBudget: 0
    });

    useEffect(() => {
        getCategories()
    }, [])

    const getCategories = async () => {
        const catResult = await retrieveCategories();
        if (catResult.status === 200){
            setCategories(catResult.data);
        }
    }

    const setCategories = (categoryDict) => {
        let categoryList = Object.keys(categoryDict).map(x => {
            return {
                "id": x, 
                "name": categoryDict[x]["name"], 
                "budget":categoryDict[x]["budget"]
            }
        });

        const validCategories = categoryList.filter(catDict => catDict["name"].length > 0);
        setState({...state, categoryList: validCategories, changesMade: false, categoryName: "", categoryBudget: 0});
    }

    const addCategory = () => {
        const url = SERVER + "api/categories";
        const formData = new FormData();
        formData.append("categoryName", JSON.stringify(state.categoryName));
        formData.append("categoryBudget", JSON.stringify(state.categoryBudget));
        const options = getRequestOptions("POST", formData);

        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((categoryDict) => {
                    setCategories(categoryDict);
                });
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
                    response.json().then((categoryDict) => {
                        setCategories(categoryDict);
                    });
                }
            });
        } else{
            console.error("Missing Row");
        }
    }

    const editCategory = (row) => {
        const url = SERVER + "api/categories";
        const formData = new FormData();

        formData.append("categoryId", JSON.stringify(row["id"]));
        formData.append("categoryName", JSON.stringify(row["name"]));
        formData.append("categoryBudget", JSON.stringify(row["budget"]));
        const options = getRequestOptions("POST", formData);

        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((categoryDict) => {
                    setCategories(categoryDict);
                });
            }
        });
    }

    return(
        <Container fluid>
            <div style={{margin: "3%"}}>
                <Row>
                    <Col sm={3}>
                        <div style={{width: "300px", float:"left"}}>
                            <Form.Label>Name</Form.Label>
                        </div>
                    </Col>
                    <Col sm={2}>
                        <div style={{width: "300px"}}>
                            <Form.Label>Budget</Form.Label>
                        </div>
                    </Col>
                </Row>
                
                <Row>
                    <Col sm={3}>
                        <Form.Control type="text"
                            onChange={(e) => setState({...state, categoryName: e.target.value})}
                            placeholder="Category name"
                            value={state.categoryName}/>
                    </Col>
                    <Col sm={2}>
                        <Form.Control type="text"
                            onChange={(e) => setState({...state, categoryBudget: validateNumbers(e.target.value)})}
                            value={state.categoryBudget}/>
                    </Col>
                    <Col sm={3}>
                        <Button variant="outline-dark center-block"
                            onClick={() => addCategory()}
                            disabled={state.categoryName == ""}>
                            Add Category
                        </Button>
                    </Col>
                </Row>
            </div>

            <div style={{margin: "3%"}}>
                <Table dataList={state.categoryList}
                    columns={getCategoriesTableColumns(deleteCategory)} 
                    changeStateData={editCategory}/>
            </div>
        </Container>
    )
}

export default Budgets