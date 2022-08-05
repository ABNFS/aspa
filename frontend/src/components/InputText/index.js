import './inputtext.css';

import React from "react";

import Label from '../Label'

class InputText extends React.Component {
    render() {
        const label = this.props.label || "Label";
        const placeholder = this.props.placeholder || "Input your text";
        const alt = this.props.alt || "Unknow input text, put you text here";
        const required = this.props.required? "required" : "label";
        const on_change = this.props.onChange
        return <div>
            <Label text={label} css_class={required}/>
            <input className="input" required={this.props.required} type="text" placeholder={placeholder} alt={alt} onChange={on_change}/>
        </div>;
    }
}

export default InputText;