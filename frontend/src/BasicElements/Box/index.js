import './box.css';

import Button from "../Button";
import { Link } from "react-router-dom";
import {useState} from "react";


function Box(props) {
    const [show, setShow] = useState(true);

    if(show){
        return (
            <div className='box' >
                <div className="modal">
                    { props.children }
                    <Link to="/"><Button type="close" label="X" action={()=> setShow(false)} /></Link>
                </div>
            </div>
        );
    }
    return "";
}

export default Box;