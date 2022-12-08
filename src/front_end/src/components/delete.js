import axios from 'axios';
import React, { Component } from 'react';

/**
 * React component of delete
 */
class Delete extends Component {

  /**
   * constructor of the component
   * @param {Object} props
   */
  constructor(props) {
    super(props);

    this.state = {
      col: 'book',
      id: '',
      code: '',
      results: ''
    }

    this.handleInDeleteChange = this.handleInDeleteChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  /**
   * the function applied when input change
   * @param {Event} event
   */
  handleInDeleteChange(event) {

    const variableName = event.target.name;
    this.setState({ [variableName]: event.target.value });
  }

  /**
   * Event handler for deleting items
   * @param {Event} event
   */
  handleSubmit(event) {
    const server_url = `http://localhost:5000/${this.state.col}?id=${this.state.id}`;
    axios.delete(
      server_url
    ).then(
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
    });
    event.preventDefault();
  }


  /**
   * render the results of Delete
   * @returns rendered results
   */
  renderDeleteResults() {
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
          <h3> Successfully Delete ! </h3>
        </div>
      )
    }
  }

  /**
   * render function for update component
   * @returns html code of upload panel
   */
  render() {
    return (
      <div>
        <h3>Delete Items</h3>
        <form
          className='update-form'
          onSubmit={this.handleSubmit}>
          <select
            name='col'
            onChange={this.handleInDeleteChange}>
            <option value='book'>Book</option>
            <option value='author'>Author</option>
          </select>

          <input
            name='id'
            type='text'
            placeholder='id'
            onChange={this.handleInDeleteChange} />

          <button
            name='Delete'
            disabled={(this.state.id === '')}
          > Delete
          </button>
        </form>
        {this.renderDeleteResults()}
      </div>
    );
  }
};

export default Delete;

