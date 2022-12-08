import axios from 'axios';
import React, { Component } from 'react';
import TopKPlot from "./plot";

/**
 * React component of update
 */
class Visualize extends Component {

  /**
   * constructor of the component
   * @param {Object} props
   */
   constructor(props){
    super(props);

    this.state = {
      col: 'book',
      k: '',
      code: '',
      results: ''
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  /**
   * the function applied when inVisualize change
   * @param {Event} event
   */
  handleInputChange(event){

    const variableName = event.target.name;
    this.setState({[variableName]: event.target.value});
  }

  /**
   * Event handler for updating items
   * @param {Event} event
   */
  handleSubmit(event) {
    const requestUrl = `http://localhost:5000/vis/${this.state.col}?k=${this.state.k}`;
    axios.get(
      requestUrl
    ).then(
      response => {
        console.log(response);
        this.setState({code: response.data.code, results: response.data.results});
      }
    ).catch(error =>{
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
   * render the results of top k items
   * @returns rendered results
   */
  renderVisualizeResults() {
    if (!this.state.code){
      return;
    }
    if (this.state.code !== 200){
        return (
            <div>
                <h2>{this.state.code}</h2>
                <h4>{this.state.results}</h4>
            </div>
        );
    } else {
        return (<div>
          <TopKPlot
        width={80 * this.state.k}
        height={200}
        top={50}
        bottom={20}
        data={this.state.results}
        col={this.state.col}
      />
    </div>);
    }

  }

  /**
   * render function for visualize component
   * @returns html response
   */
  render(){
    return (
      <div>
        <h3>Best top review items</h3>
        <form
          className='visualize-form'
          onSubmit={this.handleSubmit}>
          <select
            name='col'
            onChange={this.handleInputChange}>
            <option value='book'>Book</option>
            <option value='author'>Author</option>
          </select>

          <input
            name='k'
            type='text'
            placeholder='top k input'
            onChange={this.handleInputChange}/>

          <button
            name='Visualize'
            disabled={(this.state.k==='')}
          > Show
          </button>
      </form>
      {this.renderVisualizeResults()}
      </div>
    );
  }
};

export default Visualize;
