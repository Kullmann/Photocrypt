/*
    githublink component
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";
import GithubLogo from "../../components/GithubLogo";


export default class GithubLink extends Component{

  
  defaultSize = 80;

  render() {
      return (
        <div className="GithubLink">
            <p>
              <a href="https://github.com/Kullmann/RSAPhotoCryptography">
                Check out our github!
              </a>
            </p>
            <a href="https://github.com/Kullmann/RSAPhotoCryptography">
              <GithubLogo style={{ marginLeft: 10 }} />
            </a>
            </div>
    );
  }
}
