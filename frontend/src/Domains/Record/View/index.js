import "./recordview.css"
import Box from "../../../BasicElements/Box";
import InputText from "../../../BasicElements/InputText";
import { useState } from 'react';
import { useParams } from "react-router-dom";
import Connector from "../../../Infrastructure";

function RecordView () {
    const {id} = useParams();
    const [note, setNote] = useState();
    const [date, setDate] = useState();
    const [totalAmount, setTotalAmount] = useState(0);
    const [tags, setTags] = useState([]);
    const [accounts, setAccounts] = useState([]);


    const digits = parseInt(localStorage.getItem('digits')) || 2;
    const currency = localStorage.getItem('default_ISO') ?? 'USD';
    const operations = JSON.parse(localStorage.getItem('operations'));

    if(totalAmount===0){
        const connector = new Connector("record");
        connector.get({id}).then(s=> {return {...s}},f=>`Network Error ${f}!`).then( (record)=>{
            setNote(record.note);
            setDate(record["date"]);
            setTotalAmount(parseInt(record.total_amount));
            setTags(record.my_tags);
            setAccounts(record.accounts_record);
        });
    }

    return (<Box>
        <InputText label="Id"
                   defaultValue={id}/>
        <InputText label="Descrição" alt="informe a descrição do movimento" placeholder="descrição do movimento..."
                   on_change={e => setNote(e.target.value)} defaultValue={note}/>
        <InputText label="Data" alt="Informe a data do movimento" placeholder="data da movimentação..."
                   on_change={e => setDate(e.target.value)} defaultValue={date}/>
        <InputText label="Total" alt="informe o total envolvido" placeholder="total..."
                   type="number"
                   // on_change={e => setTotalAmount(Math.trunc(parseFloat(e.target.value,0)*10**digits))}
                   defaultValue={((totalAmount)/10**digits).toLocaleString(currency)}/>
        <InputText label="Tags" alt="" placeholder="tags..." defaultValue={tags}/>
        <table>
            <thead><tr><th>Código</th><th>Nome</th><th>Valor</th><th>Op</th><th>Tipo Conta</th></tr></thead>
            <tbody>
            {   accounts?.map( (acc, index) => (<tr key={index}>
                    <td>{acc?.account_in_record?.code}</td>
                    <td>{acc?.account_in_record?.name}</td>
                    <td>{ ((acc?.value)/10**digits).toLocaleString(currency) }</td>
                    <td>{operations.filter(v=>v.id===acc?.operation)[0].alias}</td>
                    <td> </td>
            </tr>)
            )};
            </tbody>
        </table>

    </Box>);
}

export default RecordView;