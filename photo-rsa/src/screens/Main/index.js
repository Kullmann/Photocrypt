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
    this.showAll = true;
  }

  setImage = (_image) => {
    this.setState({ image: _image });
  };

  render() {
    return (
      <div className="Container">
        <Header showall={!this.state.showAll} />
        <div className="Body">
          <RSAButton />
          <div className="ProgramButtons">
            <Upload
              setimg={this.setImage}
              buttonName="Encrypt"
              path="/encrypt"
            />
            <Upload buttonName="Upload public key" path="/loadPublicKey" />

            <Upload
              setimg={this.setImage}
              buttonName="Decrypt"
              path="/decrypt"
            />
            <Upload buttonName="Upload private key" path="/loadPrivateKey" />
          </div>
          {!this.state.image ? (
            <p>Encrypt or Decrypt a photo to see result</p>
          ) : (
            <Result image={this.state.image} setimg={this.setImage} />
          )}
        </div>
        <div className="Footer">
          <GithubLink />
        </div>
      </div>
    );
  }
}
