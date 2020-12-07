import React from 'react';
import { Nav, Navbar } from "react-bootstrap";
import './css/navigation.css'
import { Link } from 'react-router-dom';


const Navigation = () => {
    return (
        <Navbar bg="light" variant="light" expand="lg" className="navBanner">
            <Navbar.Brand style={{color: 'white'}}>
{/*                 <img */}
{/*                     src="../CIBC_DataStudioLogo.png" */}
{/*                     width="30" */}
{/*                     height="30" */}
{/*                     className="d-inline-block align-top" */}
{/*                     alt="CIBC Data Studio logo" */}
{/*                 />{' '} */}
                Budgeting Tool
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />

            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Item>
                        <Link to="/transactions" className="nav-link">Transactions</Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Link to="/categories" className="nav-link">Categories</Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Link to="/fairness" className="nav-link">Fairness Analysis</Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Link to="/model" className="nav-link">Build Model</Link>
                    </Nav.Item>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Navigation;