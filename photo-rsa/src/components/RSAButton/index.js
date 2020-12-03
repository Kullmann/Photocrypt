/*
    logo component
    author: Sean Kullmann, Hosung Lee
    date: 2020-11-26
*/
import React, { Component } from "react";
import * as axios from "axios";
import "bootstrap/dist/css/bootstrap.css";

export default class RSAButton extends Component {
  makeServerRequest = async () => {
    let path = "/generatePrivateKey";
    try {
      const res = await axios.post(path);
      console.log(res.data);
      const element = document.createElement("a");
      const file = new Blob([res.data], { type: "text/plain" });
      element.href = URL.createObjectURL(file);
      element.download = "private.pem";
      document.body.appendChild(element);
      element.click();
    } catch (err) {
      console.log("error: " + err);
    }

    path = "/generatePublicKey";
    try {
      const res = await axios.post(path);
      console.log(res.data);
      const element = document.createElement("a");
      const file = new Blob([res.data], { type: "text/plain" });
      element.href = URL.createObjectURL(file);
      element.download = "receiver.pem";
      document.body.appendChild(element);
      element.click();
    } catch (err) {
      console.log("error: " + err);
    }
  };

  render() {
    return (
      <button
        className="RSAButton btn btn-success"
        onClick={() => this.makeServerRequest()}
      >
        Generate RSA public and private key
      </button>
    );
  }
}
