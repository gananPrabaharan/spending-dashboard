import React, { useState, useEffect } from 'react'

import { Container, Row, Col, Button, Form } from 'react-bootstrap'
import { getVendorCategoriesTableColumns } from './tableColumns'
import { SERVER, getRequestOptions, validateNumbers } from './util'
import { retrieveVendorCategories, retrieveCategories } from './data'
import Table from './table'
import './css/main.css'


const Vendors = (props) => {
    const [state, setState] = useState({
        originalVendorList: [],
        vendorList: [],
        categoryDict: {},
        vendorCategoryChanges: {},
        changesMade: false
    });

    useEffect(() => {
        getVendors()
    }, [])

    const getVendors = async () => {
        let categoryDict = {};
        const catResult = await retrieveCategories();
        if (catResult.status === 200){
            categoryDict = catResult.data;
        }
//         console.info(categoryDict)

        let vendorCategories = [];
        const catVendorResult = await retrieveVendorCategories();
        if (catVendorResult.status === 200){
            vendorCategories = catVendorResult.data;
        }
//         console.info(vendorCategories)
        setData(categoryDict, vendorCategories);
    }

    const setData = (categoryDict, vendorCategories) => {
        let categoryList = Object.keys(categoryDict).map(x => {
            return {
                "id": x,
                "name": categoryDict[x]["name"],
                "budget":categoryDict[x]["budget"]
            }
        });
        let vendorList = Object.keys(vendorCategories).map(x => {
            return {
                "id": x,
                "vendor": vendorCategories[x]["vendor"],
                "categoryId": vendorCategories[x]["categoryId"]
            }
        });
//         vendorList = []
        console.info(vendorList);
        setState({...state, vendorList: vendorList, categoryDict: categoryDict, changesMade: false});
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

    const editVendorCategory = (row, oldValue, newValue) => {
        const url = SERVER + "api/vendor_categories";
        const formData = new FormData();
        formData.append("vendorId", JSON.stringify(row["vendorId"]));
        formData.append("categoryId", JSON.stringify(newValue));
        formData.append("oldCategoryId", JSON.stringify(oldValue));
        const options = getRequestOptions("POST", formData);
        fetch(url, options).then((response) => {
            if (response.status === 200){
                response.json().then((vendorCategories) => {
                    setData(state.categoryDict, vendorCategories);
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
                <Table dataList={state.vendorList}
                    columns={getVendorCategoriesTableColumns(state.categoryDict)}
                    changeStateData={editVendorCategory}/>
            </div>
        </Container>
    )
}

export default Vendors