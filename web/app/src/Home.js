import React, { Component, useState, useEffect, useRef } from 'react'
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

    .center-text {
        text-align: center;
    }

    .main-search-bar {
        padding: 32px;
        margin-top: 32px;
        margin-bottom: 8px;
    }
`


/**
 * Allows to perform search only when user
 * stopped typing (during 400 ms).
 */
function Search(props) {
    const prevProps = useRef(props); // react-hooks/exhaustive-deps
    const [searchTerm, setSearchTerm] = useState('')

    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            props.onQueryChange(searchTerm)
        }, 400)

        prevProps.current = props
        return () => clearTimeout(delayDebounceFn)
        }, [searchTerm, props]
    )

    return (
        <Form.Control
            type="text"
            placeholder={"Search " + props.nb_icons + " icons for..."}
            className={"main-search-bar"}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
    )
}


// Main component
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
        fetch(process.env.REACT_APP_API_ENDPOINT + '/api')
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

    onQueryChange = (query) => {
        this.setState({
            "query": query
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
                            <Search
                                nb_icons={this.state.nb_icons}
                                onQueryChange={this.onQueryChange}
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
