import get_url from "./urls";


function NetworkError(message = "Unknown network error") {
    this.message = message;
    this.name = "NetworkError"
}


class Connector {
    #server_info;
    #param;
    constructor(resource){
        this.#server_info = get_url(resource);
        this.#param = { mode: 'cors'}
    }

    #make_header = () => {
        const request_header = new Headers();
        const method = 'GET'? this.#param.method === undefined: this.#param.method;
        request_header.append('Access-Control-Allow-Origin', this.#server_info.server);
        request_header.append('Access-Control-Allow-Credentials', 'true');
        request_header.append('Access-Control-Allow-Methods', method);
        request_header.append('Access-Control-Allow-Headers', "Origin, Content-Type, Accept");

        request_header.append('Content-Type', 'application/json');
        request_header.append('Accept', 'application/json');
        request_header.append('Origin', this.#server_info.server);
        return request_header
    }

    #make_request = (uri=this.#server_info.uri) => {
        return new Promise( (success,fail) => {
            const myRequest = new Request(uri, this.#param);
            fetch(myRequest).then(
                (response) => {
                    if (!response.ok) {
                        throw new NetworkError(`HTTP error, status = ${response.status}`);
                    }
                    return response.json();
                }).then(
                (json_tags) => {
                    success(json_tags);
                }).catch((e) => {
                const msg = {error: e.message}
                fail(msg)
            });

        });
    }

    get = (id=-1) => {
        if(typeof(id) != 'number'){
            id = -1;
        }

        this.#param.method = "GET";
        this.#param.headers = this.#make_header();
        this.#param.body = undefined;
        return this.#make_request(`${this.#server_info.uri}/${id}`)? id<0: this.#make_request();
    }

    post = (data_to_send) => {
        this.#param.method = 'POST';
        this.#param.headers = this.#make_header();
        this.#param.body = JSON.stringify(data_to_send);
        return this.#make_request();
    }

    put = (data_to_update) => {
        this.#param.method = 'PUT';
        this.#param.headers = this.#make_header();
        this.#param.body = JSON.stringify(data_to_update);
        return this.#make_request();
    }

    delete = (id=-1) => {
        if(typeof(id) != 'number'){
            id = -1;
        }
        this.#param.method = 'DELETE';
        this.#param.headers = this.#make_header();
        return this.#make_request(`${this.#server_info.uri}/${id}`)? id<0: this.#make_request();
    }
}

export default Connector;