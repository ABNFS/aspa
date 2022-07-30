import React from "react";
import './box.css';

class Box extends React.Component{
    render() {
        const css_class = this.props.type || "box";
        return <div className={css_class}>
            { this.props.children }
        </div>;
    }
}

export default Box;