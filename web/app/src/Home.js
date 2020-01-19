import React, { Component } from 'react'
import { Container, Row, Col, Form } from 'react-bootstrap';
import styled from 'styled-components';

import Icons from './components/Icons'

const Styles = styled.div`
    .paddind-bottom {
        padding-bottom: 16px;
    }

    .center {
        width: fit-content;
        text-align: center;
        margin: 1em auto;
        display: table;
    }

    .main-search-bar {
        padding: 32px;
        margin-top: 32px;
        margin-bottom: 8px;
    }
`

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            "query": "",
            "limit": 50,
            "nb_icons": 0
        }
        this.getNbIcons()
    }

    getNbIcons = () => {
        fetch('http://localhost:5000/api')
            .then(res => res.json())
            .then((data) => {
                if (!data.error && data.details["nb_images"] !== undefined) {
                    this.setState({
                        "nb_icons": data.details["nb_images"]
                    })
                } else {
                    console.error(data)
                }
            })
            .catch(console.error)
    }

    onInputChange = (event) => {
        this.setState({
            "query": event.target.value
        })
    }

    onLimitChange = (event) => {
        this.setState({
            "limit": parseInt(event.target.value)
        })
    }

    render() {
        return (
            <Styles>
                <Container>
                    <Row className="paddind-bottom">
                        <Col lg={{ span: 12 }} className="center">
                            <Form.Control
                                type="text"
                                placeholder={"Search " + this.state.nb_icons + " icons for..."}
                                className={"main-search-bar"}
                                onChange={this.onInputChange}
                            />
                        </Col>
                        <Col lg={{ span: 2, offset: 10 }}>
                            <Form.Control
                                as="select"
                                onChange={this.onLimitChange}
                                defaultValue="50"
                            >
                                <option value="50">50</option>
                                <option value="100">100</option>
                                <option value="200">200</option>
                                <option value="400">400</option>
                            </Form.Control>
                        </Col>
                    </Row>
                    <Icons
                        key={this.state.query + this.state.limit}
                        query={this.state.query}
                        limit={this.state.limit}
                    />
                </Container>
            </Styles>
        )
    }

    componentDidMount() {
        document.title = "Home - Icons Visualizer";
    }

}

export default Home;