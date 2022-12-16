import { useState } from 'react'
import { useNavigate } from "react-router-dom";

function Bookmarks() {
    var arr = [];
    for (var i = localStorage.length - 1; i >= 0; --i ) {
        const key = localStorage.key(i);
        if (key.includes('react_search_engine')) {
            arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));   
        }
    }
    const [items, setItems] = useState(arr)

    let navigate = useNavigate(); 
    const routeChange = () => { 
        let path = `/`; 
        navigate(path);
    }

    const removeItem = (id) => {
        localStorage.removeItem('react_search_engine' + id)
        setItems([...items.filter((item) => item._id !== id)])
    }

    return (
        <div className="App">
        <header>
            <button className="bookmarks-button" onClick={routeChange}>
                back to search
            </button>
          <div className="search-input-div">
            <h1>Bookmarks</h1>
          </div>
        </header>
        <div className="search-results">
            {/* <button className="save-button" onClick={() => {}}> 
                delete all
            </button> */}
            {(items).map((item, i) => {
                return (
                    <div className="single-result">
                        <h3 className="result-title">{item._source.title}</h3>
                        <p>
                            {item._source.text}
                        </p>
                        <button className="save-button" onClick={() => removeItem(item._id)}> 
                            delete
                        </button>
                    </div>
                )
            })}
          </div>
        </div>
      );
}

export default Bookmarks;