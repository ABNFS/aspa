import './inputtext.css';

import React from "react";

import Label from '../Label'

const InputText = ( {label, placeholder, alt, required=false, on_change, id=undefined, value="", defaultValue="", type="text"}) => {
        label ??= "Label";
        placeholder ??= "Input your text";
        alt ??= "Unknow input text, put you text here";
        const required_class = required? "required" : "label";
        id ??= Math.trunc(Math.random()*10000000);
        if(defaultValue !== ""){
            return (<div>
                <Label htmlFor={id} text={label} css_class={required_class}/>
                <input id={id} className="input" type={type}
                       alt={alt}
                       readOnly={true}
                       value={defaultValue}
                />
            </div>);
        }
        return (<div>
            <Label htmlFor={id} text={label} css_class={required_class}/>
            <input id={id} className="input" required={required} type={type}
                   placeholder={placeholder} alt={alt} onChange={on_change}
                   value={value}
            />
        </div>);
}

export default InputText;