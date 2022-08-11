import "./recordview.css"
import Box from "../../../BasicElements/Box";
import InputText from "../../../BasicElements/InputText";
import { useState } from 'react';
import {useParams} from "react-router-dom";
import Connector from "../../../Infrastructure";

const RecordView = () => {
    const {id} = useParams();
    const [anotation, setAnotation] = useState("");
    const [date, setDate] = useState();
    const [totalAmount, setTotalAmount] = useState(0);
    const [tags, setTags] = useState([]);
    const [accounts, setAccounts] = useState([]);
    const moviment = new Connector("record");
    moviment.get({id}).then(s=> {return {...s}},f=>`Network Error ${f}!`).then( (record)=>{
        setAnotation(record.anotation);
        setDate(record.date);
        setTotalAmount(record.total_amount);
        setTags(record.tags);
        setAccounts(record.accounts_record);
    });
    return <Box>
        <InputText label="Id"
                   value={id}/>
        <InputText label="Descrição" alt="informe a descrição do movimento" placeholder="descrição ddo movimento..."
                   on_change={e => setAnotation(e.target.value)} value={anotation}/>
        <InputText label="Data" alt="Informe a data do movimento" placeholder="data da movimentação..."
                   on_change={e => setDate(e.target.value)} value={date}/>
        <InputText label="Total" alt="informe o total envolvido" placeholder="total..."
                   on_change={e => setTotalAmount(e.target.value)} value={totalAmount}/>
        <InputText label="Tags" alt="" placeholder="tags..."
                   on_change={e => setTags(e.target.value)} value={tags}/>
        <InputText label="Contas" alt="" placeholder="contas..."
                   on_change={e => setAccounts(e.target.value)} value={accounts}/>

    </Box>
}

export default RecordView;