/*
    upload screen
    author: Hosung Lee, Sean Kullmann
    date: 2020-10-07
*/
import React, { Component } from "react";
import ActivityIndicator from "../../components/ActivityIndicator";
import * as axios from "axios";
import "bootstrap/dist/css/bootstrap.css";

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
    const path = this.props.path;
    try {
      const res = await axios.post(path, this.state.image);
      if (path === "/encrypt") {
        await axios.post("/encryptPhoto", this.state.image);
        console.log(res.data);
        const element = document.createElement("a");
        const file = new Blob([res.data], { type: "text/plain" });
        element.href = URL.createObjectURL(file);
        element.download = "encrypted_data.bin";
        document.body.appendChild(element);
        element.click();
      }
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
        {!this.state.loading ? (
          <form className="UploadForm">
            <label className="btn btn-primary">
              <p>{this.props.buttonName}</p>
              <input
                id="file"
                type="file"
                onChange={this.onChangeImage.bind(this)}
                ref={this.imageInputRef}
              />
            </label>
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
