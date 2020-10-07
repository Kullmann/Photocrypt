/*
    github logo component
    author: Hosung Lee
    date: 2020-10-07
*/
import React, { Component } from "react";

export default class GithubLogo extends Component{

  
  defaultSize = 30;

  render() {
      return (
        <svg 
        width={this.props.size ? this.props.size : this.defaultSize} 
        height={this.props.size ? this.props.size : this.defaultSize} 
        viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"
        style={this.props.style}
        >
        <path d="M19.9975 0.416321C8.955 0.416321 0 9.40632 0 20.4963C0 29.3663 5.73 36.8913 13.68 39.5488C14.68 39.7338 15.045 39.1138 15.045 38.5813C15.045 38.1038 15.0275 36.8413 15.0175 35.1663C9.455 36.3788 8.28 32.4738 8.28 32.4738C7.3725 30.1538 6.06 29.5363 6.06 29.5363C4.2425 28.2913 6.195 28.3163 6.195 28.3163C8.2025 28.4588 9.2575 30.3863 9.2575 30.3863C11.0425 33.4538 13.94 32.5688 15.08 32.0538C15.26 30.7563 15.7775 29.8713 16.35 29.3688C11.91 28.8613 7.24 27.1388 7.24 19.4463C7.24 17.2538 8.02 15.4613 9.3 14.0563C9.0925 13.5488 8.4075 11.5063 9.495 8.74382C9.495 8.74382 11.175 8.20382 14.995 10.8013C16.59 10.3563 18.3 10.1338 20.0025 10.1263C21.7 10.1363 23.4125 10.3563 25.01 10.8038C28.8275 8.20632 30.505 8.74632 30.505 8.74632C31.595 11.5113 30.91 13.5513 30.705 14.0588C31.9875 15.4638 32.76 17.2563 32.76 19.4488C32.76 27.1613 28.085 28.8588 23.63 29.3563C24.3475 29.9763 24.9875 31.2013 24.9875 33.0738C24.9875 35.7588 24.9625 37.9238 24.9625 38.5813C24.9625 39.1188 25.3225 39.7438 26.3375 39.5463C34.275 36.8863 40 29.3638 40 20.4963C40 9.40632 31.045 0.416321 19.9975 0.416321Z" fill="#CED4E9"/>
        </svg>

    );
  }
}