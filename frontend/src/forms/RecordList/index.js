import "./recordlist.css";

import React from "react";
import Connector from "../../BackendConnector";

class RecordList extends React.Component{

    constructor(props) {
        super(props);

        this.state = { moviment : []}

    }

    componentDidMount() {
        const conn = new Connector("record");
        conn.get().then((s)=>this.setState( {moviment: s}), (f) => this.setState({erro: f}));
    }

    render() {
        console.log(this.state.moviment)
        const elements = this.state.moviment.map(i=><tr key={i.id}><td>{i.anotation}</td><td>{i.date}</td><td>{i.amount}</td></tr> );
        return <div>
            <table>
                {elements}
            </table>
        </div>;
    }
}

export default RecordList;