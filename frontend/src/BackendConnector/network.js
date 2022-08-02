import get_url from "./urls";


function NetworkError(message = "Unknown network error") {
    this.message = message;
    this.name = "NetworkError"
}


class Connector {
    #server_info;
    constructor(resource){
        this.#server_info = get_url(resource)
    }

    #make_header = (method = 'GET') => {
        const request_header = new Headers();
        request_header.append('Access-Control-Allow-Origin', this.#server_info.server);
        request_header.append('Access-Control-Allow-Credentials', 'true');
        request_header.append('Access-Control-Allow-Methods', method);
        request_header.append('Access-Control-Allow-Headers', "Origin, Content-Type, Accept");

        request_header.append('Content-Type', 'application/json');
        request_header.append('Accept', 'application/json');
        request_header.append('Origin', this.#server_info.server);
        return request_header
    }

    get = () => {
        return new Promise( (success, fail) => {
            const param = {
                method: "GET",
                mode: 'cors',
                headers: this.#make_header("GET")
            }
            const myRequest = new Request(this.#server_info.uri, param);
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
}

export default Connector;