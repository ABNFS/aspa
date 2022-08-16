import "./tagcrud.css"

import React from "react";

import Box from "../../BasicElements/Box";
import InputText from "../../BasicElements/InputText";
import Button from "../../BasicElements/Button";
import Label from "../../BasicElements/Label";

import Connector from "../../Infrastructure";

class TagCrud extends React.Component{
    constructor(props) {
        super(props);

        this.state = { tags: [], error: "", atualName: ""};

        this.submit = this.submit.bind(this);
        this.delete = this.delete.bind(this);
    }

    delete = (e) => {
        e.preventDefault();
        console.log("deleted");
    }

    submit = (e) => {
        e.preventDefault();
        if(this.state.atualName){
            const conn = new Connector('tag');
            conn.post({ name: this.state.atualName }).then((s)=>console.log('Ok'), (e)=>console.log('Nops'));
        }
    }

    componentDidMount() {
        const conn = new Connector('tag');
        conn.get().then((t)=>this.setState({tags: t}), (e)=>this.setState({tags: e}))
        return true
    }

    setAtualName = (evento) => {
        this.setState({atualName: evento.target.value});
    }

    render() {
        return (<Box>
                <form className="tagCrud" onSubmit={this.submit}>
                <InputText id="tagNome" label="Nome" required={true} value={this.state.atualName}
                           placeholder="Digite uma Tag"
                           onChange={this.setAtualName}
                           alt="Campo para incluir novas tags no sistema"/>
                <Button label="Salvar" />
                <Button label="Excluir" action={this.delete} type="danger"/>
                <Label css_class="error" text={this.state.error} />
                </form>
            </Box>);
    }
}

export default TagCrud;