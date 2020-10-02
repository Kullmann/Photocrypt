import React, { Component } from "react";
import './Test.css';

export default class Test extends Component{

  render() {
      return (
      <div className="App">
        <div className="Container">
          <h1>Photo RSA - Request Test</h1>
          <form action="http://localhost:8080" method="POST">
            <input name="message"></input><button type="submit">Send!</button>
          </form>
        </div>
      </div>
    );
  }
}
