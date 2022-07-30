import "./label.css";

import React from "react";

class Label extends React.Component{

    render() {
        const css_class = this.props.css_class || "label";
        return <div className={css_class}>
            <label>{this.props.text}</label>
        </div>;
    }
}

export default Label;