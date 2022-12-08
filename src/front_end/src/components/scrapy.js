import axios from 'axios';
import React, { Component } from 'react';

/**
 * React component of update
 */
class Scrapy extends Component {

  /**
   * constructor of the component
   * @param {Object} props
   */
   constructor(props){
    super(props);

    this.state = {
      start_url: '',
      book_num: '',
      author_num: '',
      code: '',
      results: ''
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
   * Event handler for scraping urls
   * @param {Event} event
   */
  handleSubmit(event) {
    const requestUrl = `http://localhost:5000/scrape?url=${this.state.start_url}
                                                    &book_num=${this.state.book_num}
                                                    &author_num=1000`;
    axios.post(
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
   * render the results of Scrapy
   * @returns rendered results
   */
  renderPutResults() {
    if (!this.state.code){
      return;
    }
    if (this.state.code !== 200){
        return (
            <div>
                <h2>{this.state.code}</h2>
                <h3>{this.state.results}</h3>
            </div>
        );
    } else {
        return (
            <div>
                <h3> Successfully Scrapy! </h3>
            </div>
        )
    }

  }

  /**
   * render function for scraping component
   * @returns html response
   */
  render(){
    return (
      <div>
        <h3>Scrapy</h3>
        <form
          className='update-form'
          onSubmit={this.handleSubmit}>

          <input
            name='start_url'
            type='text'
            placeholder='start url'
            onChange={this.handleInputChange}/>
          <input
            name='book_num'
            type='text'
            placeholder='book number'
            onChange={this.handleInputChange} />

          <button
            name='Scrapy'
            className={`scrapy-button ${this.state.start_url!=='' ? 'active' : null}`}
            disabled={(this.state.start_url==='')}
          > Scrapy
          </button>
      </form>


      {this.renderPutResults()}
      </div>
    );
  }
};

export default Scrapy;
