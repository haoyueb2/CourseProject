import React, { Component } from 'react';
// import col from './col';
import axios from 'axios';
import BookTemplate from "./bookTemplate";

/**
 * Search Query Component
 */
class SearchQuery extends Component {

  /**
   * constructor of the component
   * @param {Object} props
   */
  constructor(props){
    super(props);
    this.state = {
      query: '',
      code: '',
      results: ''
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }



  /**
   * Event handler for submitting a query
   * @param {Event} event
   */
  handleSubmit(event) {
    console.log(this.state.query)
    axios.get(
        `http://localhost:5000/search?q=${this.state.query}`,
      ).then(
        response => {
          console.log(response);
          this.setState({code: response.data.code, results: response.data.results});
        }
      ).catch(error => {
        console.log(error.response);
        this.setState({
          code: error.response.data.code,
          results: error.response.data.results
        });
      });
    event.preventDefault();
  }

  /**
   * the function applied when input change
   * @param {Event} event
   */
  handleInputChange(event){
    const variableName = event.target.name;
    this.setState({[variableName]: event.target.value});
  }

  /**
   * render search results
   * @returns html code of search results
   */
  renderSearchResults() {
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
      console.log(this.state.results)
      if ('book_id' in this.state.results[0]){
        return (<BookTemplate
                results={this.state.results}
        />);
      }

    }

  }

  /**
   * search id renderer
   * @returns html response
   */
  render(){
    return (
      <div>
        <h3>Search a book based on name</h3>
        <form
          className='search-form'
          onSubmit={this.handleSubmit}>

          <div>
          <input
            name='query'
            type='text'
            placeholder='query'
            onChange={this.handleInputChange}/>
          </div>

          <button
            type='submit'
            className={`search-button ${this.state.query!=='' ? 'active' : null}`}
            disabled={this.state.query===''}
          > Search Name
          </button>
      </form>

      {this.renderSearchResults()}
      </div>
    );
  }
};

export default SearchQuery;
