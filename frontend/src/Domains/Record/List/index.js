import "./recordlist.css";

import React, {useState} from "react";
import Connector from "../../../Infrastructure";
import { Outlet, Link} from "react-router-dom";

function RecordList () {
    const [movement, setMovement] = useState([]);

    const makeElementsRow = (mov=[]) => {
        const digits = localStorage.getItem('digits');
        const currency = localStorage.getItem('default_ISO');
        return mov.map((item, index)=>{ return (
            <tr key={item.id} className="recordListRow">
                <td className="recordListColumnText" tabIndex={(index+1)*10+1}>{item.note}</td>
                <td className="recordListColumnDate" tabIndex={(index+1)*10+2}>{item.date}</td>
                <td className="recordListColumnMoney" tabIndex={(index+1)*10+3}>{Number(item.total_amount/(10**digits)).toLocaleString('BR', { style: 'currency', currency: currency})}</td>
                <td className="recordListColumnOptions">
                    <Link to={`record-view\\${item.id}`}><span className="view" tabIndex={(index+1)*10+4}/></Link>
                    <Link to={`record-edit\\${item.id}`}><span className="edit" tabIndex={(index+1)*10+5}/></Link>
                    <Link to={`record-delete\\${item.id}`}><span className="delete" tabIndex={(index+1)*10+6}/></Link>
                </td>
            </tr>);});
    };

    const makeTable = (rows=[]) => {
        return <>
            <table className="recordListTable">
                <thead className="recordListHead">
                <tr>
                    <th tabIndex={1}>Observação</th>
                    <th tabIndex={2}>Data</th>
                    <th tabIndex={3}>Valor</th>
                    <th tabIndex={4}>Opções</th>
                </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
            <Outlet/>
        </>;
    }

    let elements = makeElementsRow(movement);

    if(elements.length === 0){
        const movementConnector = new Connector("record");
        movementConnector.get().then(s=>setMovement(s)).then(s=>elements = makeElementsRow(movement));
        return makeTable(elements);
    }
    else {
        return makeTable(elements);
    }
}

export default RecordList;