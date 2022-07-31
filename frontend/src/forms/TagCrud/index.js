import "./tagcrud.css"

import React from "react";

import Box from "../../components/Box";
import InputText from "../../components/InputText";
import Button from "../../components/Button";
import Label from "../../components/Label";

class TagCrud extends React.Component{
    constructor(props) {
        super(props);

        this.state = { tags: [], error: ""};

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
        console.log('submited');
    }

    componentDidMount() {
        const url = "http://127.0.0.1:8000/tag/";

        const request_header = new Headers();
        request_header.append('Access-Control-Allow-Origin', 'http://localhost:3000');
        request_header.append('Access-Control-Allow-Credentials', 'true');
        request_header.append('Access-Control-Allow-Methods', "GET");
        request_header.append('Access-Control-Allow-Headers', "Origin, Content-Type, Accept");

        request_header.append('Content-Type', 'application/json');
        request_header.append('Accept', 'application/json');
        request_header.append('Origin', 'http://localhost:3000');

        const param = {
            method: "GET",
            mode: 'cors',
            headers: request_header
        }

        const myRequest = new Request(url, param);

        fetch(myRequest).then(
            (response)=>{
                if(!response.ok){
                    throw new Error(`HTTP error, status = ${response.status}`);
                }
                console.log(response);
                return response.json();
            }).then(
                (t)=>{
                    this.setState({tags: t})
                    console.log(t);
                }).catch((e)=>this.setState({error:e.message}));
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
                </form>
            </Box>);
    }
}

export default TagCrud;