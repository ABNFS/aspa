import './button.css';

import React from "react";

class Button extends React.Component {

    render() {
        const action = this.props.action ?? false;
        const label = this.props.label ?? 'Label Here!';
        const type = this.props.type ?? "button";

        return <button className={type} onClick={(e)=>{if(action){action(e);}}}>{label}</button>;

    }
}

export default Button;