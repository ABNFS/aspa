import './inputtext.css';

import React from "react";

import Label from '../Label'

const InputText = ( {label, placeholder, alt, required=false, on_change, id=undefined, value=""}) => {
        label ??= "Label";
        placeholder ??= "Input your text";
        alt ??= "Unknow input text, put you text here";
        const required_class = required? "required" : "label";
        id ??= Math.floor(Math.random()*10000000);
        return <div>
            <Label htmlFor={id} text={label} css_class={required_class}/>
            <input id={id} className="input" required={required} type="text"
                   placeholder={placeholder} alt={alt} onChange={on_change}
                   value={value}
            />
        </div>;
}

export default InputText;