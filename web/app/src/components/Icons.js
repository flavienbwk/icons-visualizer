import React, { Component } from 'react'
import { Row, Col, Card } from 'react-bootstrap'
import PropTypes from 'prop-types'
import tersus from 'tersus-jsx.macro'

export default class Icons extends Component {

    constructor(props) {
        super(props)
        this.state = {
            "onChange": null,
            "query": props.query,
            "icons": [],
            "limit": 50
        }
        this.getIconsFromQuery()
    }

    getIconsFromQuery = () => {
        const query = this.props.query?.trim()
        if (query) {
            fetch('http://localhost:5000/api/icons/' + query + '/' + this.props.limit)
                .then(res => res.json())
                .then((data) => {
                    if (!data.error && data.details.length) {
                        this.setState({
                            "icons": data.details
                        }, () => {
                            if (this.props.onChange)
                                this.props.onChange(data.details.length)
                        })
                    } else {
                        console.error(data)
                    }
                })
                .catch(console.error)
        }
    }

    render() {
        return tersus(
            (this.state.icons.length)
                ?
                <Row className="center-text">
                    <Col lg={{ span: 12 }}>
                        <Card>
                            <Card.Body>
                                <Card.Title>Found {this.state.icons.length} icon{(this.state.icons.length > 1) ? "s" : ""}</Card.Title>
                                <Card.Text>Related to <b>{this.state.query}</b></Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                    {
                        this.state.icons.map((icon) => {
                            return (
                                <Col lg={{ span: 3 }} key={icon.id} style={{ marginTop: 16 }}>
                                    <Card>
                                        <Card.Img
                                            variant="top"
                                            src={"http://localhost:5000/icon/" + icon.id}
                                            className={"center"}
                                            style={{ width: 64 }}
                                        />
                                        <Card.Body>
                                            <Card.Text>
                                                {icon.filename}
                                            </Card.Text>
                                            <a
                                                className={"btn btn-secondary"}
                                                href={"http://localhost:5000/icon/" + icon.id}
                                                download
                                            >
                                                Download
                                            </a>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            )
                        })
                    }
                </Row>
                :
                <h2>No icon was found, start a new search.</h2>
        )
    }

}

Icons.propTypes = {
    query: PropTypes.string,
    limit: PropTypes.number
}
