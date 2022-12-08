import React, { Component } from 'react';
// import col from './col';
import axios from 'axios';

class Export extends Component {

    constructor(props) {
        super(props);
        this.state = {
            code: '',
            results: ''
        }
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        const requestUrl = 'http://localhost:5000/export';
        axios.get(requestUrl).then(
            response => {
                console.log(response);
                this.setState({ code: response.data.code, results: response.data.results });
            }
        ).catch(error => {
            console.log(error.response);
            if (error.response) {
                this.setState({
                    code: error.response.data.code,
                    results: error.response.data.results
                });
            }
        })
    }

    renderPutResults() {
        if (!this.state.code) {
            return;
        }
        if (this.state.code !== 200) {
            return (
                <div>
                    <h2>{this.state.code}</h2>
                    <h3>{this.state.results}</h3>
                </div>
            );
        } else {
            return (
                <div>
                    <h3> Successfully Export! </h3>
                </div>
            )
        }
    }
    render() {
        return (
            <div>
                <h3>Export database to json</h3>
                <form
                    className='update-form'
                    onSubmit={this.handleSubmit}>
                    <button
                        name='Export'
                    > Export
                    </button>
                </form>

                {this.renderPutResults()}
            </div>
        );
    }
}

export default Export;