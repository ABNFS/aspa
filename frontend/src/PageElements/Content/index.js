import "./content.css"
import RecordList from "../../Domains/Record/List";
import { Route, Routes } from "react-router-dom";
import TagCrud from "../../Domains/TagCrud";
import RecordEdit from "../../Domains/Record/Edit";
import RecordView from "../../Domains/Record/View";
import RecordDelete from "../../Domains/Record/Delete";
import Connector from "../../Infrastructure";


const makeLocalStorageBasicData = () => {
    if(!localStorage.getItem('digitis')){
        const digitsConnector = new Connector("digits");
        digitsConnector.get().then(s=>localStorage.setItem('digits', s));
    }
    if(!localStorage.getItem('default_ISO')){
        const defaultCurrencyConnector = new Connector("currency");
        defaultCurrencyConnector.get({default: true}).then(s=>localStorage.setItem('default_ISO', s[0]?.iso_code ?? 'USD'));
    }
    if(!localStorage.getItem('operations')){
        const operationConnector = new Connector("operation-type")
        operationConnector.get().then(s=>localStorage.setItem('operations', JSON.stringify(s)));
    }
    if(!localStorage.getItem('account_type')){
        const operationConnector = new Connector("account-type")
        operationConnector.get().then(s=>localStorage.setItem('account_type', JSON.stringify(s)));
    }
    if(!localStorage.getItem('account')){
        const operationConnector = new Connector("account")
        operationConnector.get().then(s=>localStorage.setItem('account', JSON.stringify(s)));
    }
}

const Content = () => {
    makeLocalStorageBasicData();

    return <main>
        <Routes>
            <Route path="/" element={<RecordList />}>
                <Route path="tag" element={<TagCrud />} />
                <Route path="record-edit" element={<RecordEdit/>} />
                <Route path="record-view/:id" element={<RecordView/>} />
                <Route path="record-delete" element={<RecordDelete/>} />
            </Route>
        </Routes>

    </main>
}

export default Content;