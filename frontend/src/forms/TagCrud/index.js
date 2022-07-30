import "./tagcrud.css"

import React from "react";

import Box from "../../components/Box";
import InputText from "../../components/InputText";
import Button from "../../components/Button";

class TagCrud extends React.Component{
    constructor(props) {
        super(props);
        this.save = this.save.bind(this);
        this.delete = this.delete.bind(this);
    }
    save = (e) => {
        e.preventDefault();
        console.log("saved");
    }

    delete = (e) => {
        e.preventDefault();
        console.log("deleted");
    }

    render() {
        return <div className="tagCrud">
            <Box>
                <InputText label="Nome" required={true}
                           placeholder="Digite uma Tag"
                           alt="Campo para incluir novas tags no sistema"/>
                <Button label="Salvar" action={this.save} />
                <Button label="Excluir" action={this.delete} type="danger"/>
            </Box>
        </div>;
    }
}

export default TagCrud;