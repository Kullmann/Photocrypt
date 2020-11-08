/*
    main screen
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";
import GithubLogo from "../../components/GithubLogo";
import Logo from "../../components/Logo";
import ActivityIndicator from "../../components/ActivityIndicator";
import * as axios from "axios";

export default class Main extends Component {
  constructor() {
    super();
    this.state = { loading: false, image: "", eImage: false };
    this.imageInputRef = React.createRef();
  }

  onChangeImage = (event) => {
    let reader = new FileReader();

    reader.onloadend = () => {
      const base64 = reader.result;
      if (base64) {
        this.setState({ image: base64.toString() });
        //console.log(base64.toString());
        this.makeServerRequest();
      }
    };
    if (event.target.files[0]) {
      reader.readAsDataURL(event.target.files[0]);
    }
    this.setState({ loading: true });
  };

  makeServerRequest = async () => {
    try {
      const res = await axios.post("/encrypt", this.state.image);
      const str = Buffer.from(res.data, "binary"); //.toString("base64");
      console.log(str);
      this.setState({ loading: false, image: str, eImage: true });
      this.state.document = true;
    } catch (err) {
      console.log("error: " + err);
    }
  };

  render() {
    return (
      <div className="Container">
        <div className="Header">
          <div className="Title">
            <Logo style={{ marginRight: 15 }} />
            <div class="TitleContent">
              <p className="TitleText">Encrypt Your Photo!</p>
              <p className="SubtitleText">
                Created by Sean Kullmann and Hosung Lee
              </p>
              {this.state.eImage ? (
                <img src={"data:image/bmp;base64," + this.state.image}></img>
              ) : (
                <p>Please upload an image!</p>
              )}
            </div>
          </div>
          <div className="Description">
            <p>This Web Based App encrypts your photo using RSA</p>
            <p>and draws an image that represents your encrypted photo data.</p>
          </div>
        </div>
        <div className="Content">
          <div>
            <p className="Message">Give it a try! Press the Button below</p>
            {!this.state.loading ? (
              <form className="UploadForm">
                <label class="UploadButton">
                  <p>Upload</p>
                  <input
                    id="imageInput"
                    type="file"
                    onChange={this.onChangeImage.bind(this)}
                    ref={this.imageInputRef}
                  />
                </label>
                <div className="Option">
                  <input type="checkbox"></input>
                  <a>I want to decrypt my cypherphoto.</a>
                </div>
              </form>
            ) : (
              <div className="UploadForm">
                <ActivityIndicator />
              </div>
            )}
          </div>
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
