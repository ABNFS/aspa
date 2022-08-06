import "./recordlist.css";

import React from "react";
import Connector from "../../BackendConnector";

class RecordList extends React.Component{

    constructor(props) {
        super(props);

        this.state = { moviment : [], digits: 2, currency: 'USD'}

    }

    componentDidMount() {
        const moviment = new Connector("record");
        const digits = new Connector("digits");
        const default_currency = new Connector("currency");
        moviment.get().then((s)=>this.setState( {moviment: s}), (f) => this.setState({erro: f}));
        digits.get().then((s)=>this.setState( {digits: s}), (f) => this.setState({erro: f}));
        default_currency.get({default: true}).then((s)=>this.setState( {currency: s.iso_code}), (f) => this.setState({erro: f}));
    }

    render() {
        const digits = parseInt(this.state.digits);
        const currency = this.state.currency;
        const elements = this.state.moviment.map(i=><tr key={i.id} className="recordListRow">
            <td className="recordListColumnText">{i.anotation}</td>
            <td className="recordListColumnDate">{i.date}</td>
            <td className="recordListColumnMoney">{Number(i.total_amount/(10**digits)).toLocaleString('BR', { style: 'currency', currency: currency})}</td>
            <td className="recordListColumnOptions"><span className="view" /><span className="edit" /><span className="delete" /></td></tr> );
        return <div>
            <table className="recordListTable">
                <thead className="recordListHead"><tr><th>Observação</th><th>Data</th><th>Valor</th><th></th></tr></thead>
                <tbody>{elements}</tbody>
            </table>
        </div>;
    }
}

export default RecordList;