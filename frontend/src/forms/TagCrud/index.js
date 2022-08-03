import "./tagcrud.css"

import React from "react";

import Box from "../../components/Box";
import InputText from "../../components/InputText";
import Button from "../../components/Button";
import Label from "../../components/Label";

import Connector from "../../BackendConnector";

class TagCrud extends React.Component{
    constructor(props) {
        super(props);

        this.state = { tags: [], error: "", atualName: "Alysson"};

        this.submit = this.submit.bind(this);
        this.delete = this.delete.bind(this);
        this.close = this.close.bind(this);
    }

    close = (e) => {
        e.preventDefault();
        console.log("fechou");
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

    render() {
        return (<Box>
                <form className="tagCrud modal" onSubmit={this.submit}>
                    <Button type="close" label="X" action={this.close} />
                <InputText label="Nome" required={true}
                           placeholder="Digite uma Tag"
                           alt="Campo para incluir novas tags no sistema"/>
                <Button label="Salvar" />
                <Button label="Excluir" action={this.delete} type="danger"/>
                <Label css_class="error" text={this.state.error} />
                </form><div>{JSON.stringify(this.state.tags)}</div>
            </Box>);
    }
}

export default TagCrud;