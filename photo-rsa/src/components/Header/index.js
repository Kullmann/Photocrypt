/*
    logo component
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";

import Logo from "../../components/Logo";

export default class Header extends Component{

  render() {
      return (
        <div className={this.props.showall ? "Header" : "HeaderReduced"}>
          <div className="Title">
            <Logo style={{ marginRight: 15 }} />
            <div class="TitleContent">
              <p className="TitleText">Encrypt Your Photo!</p>
              <p className="SubtitleText">
                Created by Sean Kullmann and Hosung Lee
              </p>
            </div>
          </div>
          {this.props.showall ? (
            <div className="Description">
              <p>This App encrypts your photo using AES and RSA</p>
              <p>
                and draws an image that represents your encrypted photo data.
              </p>
            </div>
          ) : (
            <></>
          )}
        </div>
    );
  }
}
