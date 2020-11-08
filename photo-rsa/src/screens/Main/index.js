/*
    main screen
    author: Hosung Lee, Sean Kullmann
    date: 2020-10-07
*/
import React, { Component } from "react";
import GithubLogo from "../../components/GithubLogo";
import Logo from "../../components/Logo";
import Upload from "../../components/Upload"
import Result from "../../components/Result"

export default class Main extends Component {
  constructor() {
    super();
    this.state = { loading: false, image: "" };
    this.imageInputRef = React.createRef();
  }

  setImage = (_image) => {
    this.setState({image: _image});
  }

  render() {
    return (
      <div className="Container">
        <div className={!this.state.image ? "Header" : "HeaderReduced"}>
          <div className="Title">
            <Logo style={{ marginRight: 15 }} />
            <div class="TitleContent">
              <p className="TitleText">Encrypt Your Photo!</p>
              <p className="SubtitleText">
                Created by Sean Kullmann and Hosung Lee
              </p>
            </div>
          </div>
          {!this.state.image?<div className="Description">
            <p>This Web Based App encrypts your photo using RSA</p>
            <p>and draws an image that represents your encrypted photo data.</p>
          </div>:<></>}
        </div>
        <div className="Content">
          {!this.state.image ? <Upload setimg={this.setImage}/> : <Result image={this.state.image} setimg={this.setImage}/>}
          <div className="Footer">
            <p>
              <a href="https://github.com/Kullmann/RSAPhotoCryptography">
                Check out our github!
              </a>
            </p>
            <a href="https://github.com/Kullmann/RSAPhotoCryptography">
              <GithubLogo style={{ marginLeft: 10 }} />
            </a>
          </div>
        </div>
      </div>
    );
  }
}
