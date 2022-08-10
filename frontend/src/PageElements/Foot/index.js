import "./foot.css"


const Foot = ({ url }) => {
        url ??= "https://ab78.cc";
        return <footer className="footer">
            <a href={url}><span className="copyright"></span></a>
        </footer>;
}

export default Foot;