/**
 * Follow the template of an example provided by react:
 * https://github.com/Yog9/SnapShot/
 */

import React, { Component } from "react";
import { HashRouter, Route, Switch } from "react-router-dom";
import SearchQuery from "./components/searchQuery";
import Navigation from "./components/navigation";
import Delete from "./components/delete";
import Scrapy from "./components/scrapy";
import Export from "./components/export";
import Visualize from "./components/visualize";
import "./App.css"

class App extends Component {
  /**
   * The render of the start page
   * @returns start page html
   */
  render() {
    return (
        <HashRouter>
          <div className="container">
            <Route
              render={props => (
                <div>
                <h1> CS410 Final Project </h1>
                <img alt="figure" src="book.png" height={250} className="img"></img>
                  <Navigation/>
                </div>
              )}
            />
            <Switch>
            <Route path="/Scrapy" render={() => <Scrapy />} />
            <Route path="/Visualize" render={() => <Visualize />} />
                <Route path="/searchQuery" render={() => <SearchQuery/>} />
                <Route path="/Delete" render={() => <Delete/>} />
            <Route path="/export" render={() => <Export />} />
            </Switch>
          </div>
        </HashRouter>
    );
  }
}

export default App;