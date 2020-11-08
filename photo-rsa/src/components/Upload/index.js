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
    this.state = { loading: false, image: "" };
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
      this.setState({ loading: false, image: ""});
      this.props.setimg(str);
      this.state.document = true;
    } catch (err) {
      console.log("error: " + err);
    }
  };

  render() {
    return (
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
    );
  }
}
