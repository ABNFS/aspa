import "./App.css"
import Head from "./page/Head";
import Foot from "./page/Foot";
import RecordList from "./forms/RecordList";
import TagCrud from "./forms/TagCrud";

function App() {
  return (
      <div className="App">
        <Head/>
        <RecordList />
        <Foot/>
      </div>

  );
}

export default App;
