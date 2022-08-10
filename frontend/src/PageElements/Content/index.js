import "./content.css"
import RecordList from "../../Domains/Record/List";
import { Route, Routes } from "react-router-dom";
import TagCrud from "../../Domains/TagCrud";
import RecordEdit from "../../Domains/Record/Edit";
import RecordView from "../../Domains/Record/View";
import RecordDelete from "../../Domains/Record/Delete";

const Content = () => {
    return <main>
        <Routes>
            <Route path="/" element={<RecordList />}>
                <Route path="tag" element={<TagCrud />} />
                <Route path="record-edit" element={<RecordEdit/>} />
                <Route path="record-view/:id" element={<RecordView />} />
                <Route path="record-delete" element={<RecordDelete/>} />
            </Route>
        </Routes>

    </main>
}

export default Content;