const server = 'http://localhost'
const port = '8000'
const backend_resources = ["account", "account-type", "operation-type", "currency", "exchange", "tag", "record"];

function UrlResourceException(message){
    this.message = message;
    this.name = "UrlResourceException";
}

function get_url(resource){
    if(!resource){
        throw new UrlResourceException('Please send a valid Resource!');
    }
    // if(!(backend_resources.map((i)=>i==resource).reduce((v)=>v))){
    //     throw new UrlResourceException("Unknown resource");
    // }
    const service = `${server}:${port}`
    return { server: service, uri: encodeURI(`${service}/${resource}`) }
}

export default get_url;