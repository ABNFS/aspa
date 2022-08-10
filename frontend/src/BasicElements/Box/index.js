import React from "react";

import './box.css';
import Button from "../Button";
import { Link } from "react-router-dom";


class Box extends React.Component{

    constructor(props) {
        super(props);

        this.state = { show: true }
    }
    close = () => {
        this.setState( {show: false});
    }

    render() {
        if(this.state.show){
            return (
                <div className='box' >
                    <div className="modal">
                        { this.props.children }
                        <Link to="/"><Button type="close" label="X" action={()=> this.close()} /></Link>
                    </div>
                </div>
            );
        }
        return "";
    }
}

export default Box;