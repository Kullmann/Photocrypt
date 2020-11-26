/*
    main screen
    author: Hosung Lee, Sean Kullmann
    date: 2020-10-07
*/
import React, { Component } from "react";
import Upload from "../../components/Upload";
import Result from "../../components/Result";
import GithubLink from "../../components/GithubLink";
import RSAButton from "../../components/RSAButton";
import Header from "../../components/Header";

export default class Main extends Component {
  constructor() {
    super();
    this.state = { image: "" };
  }

  setImage = (_image) => {
    this.setState({ image: _image });
  };

  render() {
    return (
      <div className="Container">
        <Header showall={!this.state.image}/>
        <div className="Content">
          {!this.state.image ? (
            <Upload setimg={this.setImage} />
          ) : (
            <Result image={this.state.image} setimg={this.setImage} />
          )}
          <RSAButton/>
          {false ? <GithubLink/> : <></>}
        </div>
      </div>
    );
  }
}
