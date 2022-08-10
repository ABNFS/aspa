import "./recordlist.css";

import React from "react";
import Connector from "../../../Infrastructure";
import { Outlet, Link} from "react-router-dom";

class RecordList extends React.Component{

    constructor(props) {
        super(props);

        this.state = {
            moviment : [],
            digits: 2,
            currency: 'USD'
        }

    }

    componentDidMount() {
        const moviment = new Connector("record");
        const digits = new Connector("digits");
        const default_currency = new Connector("currency");
        moviment.get().then((s)=>this.setState( {moviment: s}), (f) => this.setState({erro: f}));
        digits.get().then((s)=>this.setState( {digits: s}), (f) => this.setState({erro: f}));
        default_currency.get({default: true}).then((s)=>this.setState( {currency: s[0].iso_code}), (f) => this.setState({erro: f}));
    }

    render() {
        const digits = parseInt(this.state.digits);
        const currency = this.state.currency;
        const elements = this.state.moviment.map((item, index)=>{ return (
            <tr key={item.id} className="recordListRow">
                <td className="recordListColumnText" tabIndex={(index+1)*10+1}>{item.anotation}</td>
                <td className="recordListColumnDate" tabIndex={(index+1)*10+2}>{item.date}</td>
                <td className="recordListColumnMoney" tabIndex={(index+1)*10+3}>{Number(item.total_amount/(10**digits)).toLocaleString('BR', { style: 'currency', currency: currency})}</td>
                <td className="recordListColumnOptions">
                    <Link to={`record-view\\${item.id}`}><span className="view" tabIndex={(index+1)*10+4}/></Link>
                    <Link to={`record-edit\\${item.id}`}><span className="edit" tabIndex={(index+1)*10+5}/></Link>
                    <Link to={`record-delete\\${item.id}`}><span className="delete" tabIndex={(index+1)*10+6}/></Link>
                </td>
            </tr>);});
        return <>
            <table className="recordListTable">
                <thead className="recordListHead"><tr><th tabIndex={1}>Observação</th><th tabIndex={2}>Data</th><th tabIndex={3}>Valor</th><th tabIndex={4}>Opções</th></tr></thead>
                <tbody>{elements}</tbody>
            </table>
            <Outlet />
        </>;
    }
}

export default RecordList;