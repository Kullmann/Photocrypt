/*
    upload screen
    author: Hosung Lee, Sean Kullmann
    date: 2020-10-07
*/
import React, { Component } from "react";
import ActivityIndicator from "../../components/ActivityIndicator";
import * as axios from "axios";

export default class Upload extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false, image: "", encrypt: true };
    this.imageInputRef = React.createRef();
  }

  onChangeImage = (event) => {
    let reader = new FileReader();

    reader.onloadend = () => {
      const base64 = reader.result;
      if (base64) {
        this.setState({ image: base64.toString() });
        this.makeServerRequest();
      }
    };
    if (event.target.files[0]) {
      reader.readAsDataURL(event.target.files[0]);
    }
    this.setState({ loading: true });
  };

  makeServerRequest = async () => {
    const path = this.state.encrypt ? "/encrypt" : "/decrypt";
    try {
      const res = await axios.post(path, this.state.image);
      const str = Buffer.from(res.data, "binary");
      console.log(str);
      this.setState({ loading: false, image: "" });
      this.props.setimg(str);
    } catch (err) {
      console.log("error: " + err);
    }
  };

  toggleCipher = () => {
    this.setState({ encrypt: !this.state.encrypt });
  };

  render() {
    return (
      <div>
        <p className="Message">
          Give it a try! Press the button below to upload a photo.
        </p>
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
              <input type="checkbox" onChange={this.toggleCipher}></input>
              <a>I want to decrypt my cypherphoto.</a>
            </div>
          </form>
        ) : (
          <div className="UploadForm">
            <ActivityIndicator />
          </div>
        )}
      </div>
    );
  }
}
