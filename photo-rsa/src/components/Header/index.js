/*
    logo component
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";
import Logo from "../../components/Logo";

export default class Header extends Component {
  constructor() {
    super();
    this.showAll = true;
  }

  render() {
    return (
      <div className={this.props.showall ? "Header" : "HeaderReduced"}>
        <div className="Title">
          <Logo style={{ marginRight: 15 }} />
          <div
            className="TitleContent"
            style={{ alignItems: "center", justifyContent: "center" }}
          >
            <p className="TitleText">
              AES-128 Photo Encryption wrapped with RSA-2048
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
