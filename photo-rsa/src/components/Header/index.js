/*
    logo component
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";
import Upload from "../../components/Upload";
import Result from "../../components/Result";
import GithubLink from "../../components/GithubLink";
import RSAButton from "../../components/RSAButton";

import Logo from "../../components/Logo";

export default class Header extends Component {
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
      <div className={this.props.showall ? "Header" : "HeaderReduced"}>
        <div className="Title">
          <Logo style={{ marginRight: 15 }} />
          <div
            class="TitleContent"
            style={{ alignItems: "center", justifyContent: "center" }}
          >
            <p className="TitleText">
              AES-256 Photo Encryption wrapped with RSA-2048
            </p>
            <p className="SubtitleText">
              Created by Sean Kullmann and Hosung Lee
            </p>
          </div>
        </div>
      </div>
    );
  }
}
