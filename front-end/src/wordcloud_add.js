import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { createCloud, getCloudStatus } from './apis';

import './wordcloud_add.css';
import Spinner from 'react-bootstrap/Spinner';

class AddForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.state = {
            isLoading: false,
            errors: null,
            cloudId: null,
            show: false
        };
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.state.cloudId !== prevState.cloudId && !prevState.cloudId) {
            this.initPingLoop();
        }
    }

    initPingLoop() {
        const handleCallback = () => {
            if (!this.state.cloudId)
                return;
            getCloudStatus(this.state.cloudId).then(response => {
                if (response['error_msg']) {
                    // display error
                    this.setState({error: response['error_msg'], loading: false, cloudId: null});
                }
                else if (response['is_generated']) {
                    // redirect to homepage
                    document.location.href = "/";
                }
                else {
                    // wait a few seconds and call again
                    setTimeout(handleCallback, 10000);
                }
            });
        };
        handleCallback();
    }

    handleSubmit(e=null) {
        if (e) e.preventDefault();
        const formTitle = this.refs.cloudTitle.value;
        const formText = this.refs.cloudText.value;
        createCloud(formTitle, formText)
            .then((response) => {
                this.setState({cloudId: response.id})
            })
            .catch(error => {
                this.setState({error, isLoading: false});
            });
        this.setState({isLoading: true});
    }

    handleShow() {
        this.setState({show: true});
    }

    handleClose() {
        this.setState({show: false});
    }

    renderErrors() {
        return (
            <label className="errors">{(this.state.error) ? `Error: ${this.state.error}` : ''}</label>
        )
    }

    renderForm() {
        const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed...."
        return (
            <Form onSubmit={this.handleSubmit}>
                {this.renderErrors()}
                <Form.Group controlId="form.title">
                    <Form.Label>Title</Form.Label>
                    <Form.Control ref="cloudTitle" type="text" placeholder="Enter title" />
                </Form.Group>

                <Form.Group controlId="form.text">
                    <Form.Label>WordCloud Text</Form.Label>
                    <Form.Control ref="cloudText" as="textarea" rows="9" placeholder={loremIpsum}/>
                    <Form.Text className="text-muted">
                        This might take a few minutes.
                    </Form.Text>
                </Form.Group>
            </Form>
        );
    }

    render() {
        const isWaiting = !!this.state.cloudId || this.state.isLoading;
        return (
            <div className="add-form">
                <button id="add" className={this.state.show ? 'active': ''} onClick={this.handleShow}>
                    <img id="addSign"
                         src="https://ssl.gstatic.com/bt/C3341AA7A1A076756462EE2E5CD71C11/2x/btw_ic_speeddial_white_24dp_2x.png"
                         alt="add" />
                </button>

                <Modal show={this.state.show} onHide={this.handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>New Word Cloud</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {this.renderForm()}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleClose} disabled={isWaiting}>
                            Close
                        </Button>
                        <Button variant="primary" onClick={this.handleSubmit} disabled={isWaiting}>
                            Create {(isWaiting) ? <Spinner animation="border" role="status" size="sm"><span className="sr-only">Loading...</span></Spinner> : ''}
                        </Button>
                    </Modal.Footer>
                </Modal>
            </div>
        );
    }
}

export default AddForm;
