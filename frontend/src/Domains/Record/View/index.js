import "./recordview.css"
import Box from "../../../BasicElements/Box";
import InputText from "../../../BasicElements/InputText";
import { useState } from 'react';
import {useParams} from "react-router-dom";
import Connector from "../../../Infrastructure";

const RecordView = () => {
    const { id } = useParams();
    const [descricao, setDescricao] = useState(id);
    let record = {};
    let error = "";
    const moviment = new Connector("record");
    moviment.get({id}).then(s=>record={...s}, f=>error=`Network Error ${f}!`);
    console.log(record);
    return <Box>
        <InputText label="Descrição" alt="informe a descrição da despesa" placeholder="descrição da despesa..."
                   on_change={e=>setDescricao(e.target.value)} value={descricao}/>
    </Box>
}

export default RecordView;