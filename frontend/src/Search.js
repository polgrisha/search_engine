import { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";

function Search() {
    const [search, setSearch] = useState("")
    const [results, setResults] = useState([])

    let navigate = useNavigate(); 
    const routeChange = () => { 
        let path = `/bookmarks`; 
        navigate(path);
    }

    const handleSearch = async e => {
        e.preventDefault();
        if (search === '') return

        console.log(search)
    
        const url = `/search?q=${search}`
        const res = await fetch(url)
        const json_res = await res.json()

        console.log(json_res)
        setResults(json_res.hits.hits)

        console.log(results)
    }

    function saveItem(item) {
        localStorage.setItem('react_search_engine' + item._id, JSON.stringify(item));
    }

    return (
    <div className="App">
    <header>
      <button className="bookmarks-button" onClick={routeChange}>
        bookmarks
      </button>
      <div className="search-input-div">
        <h1>My search engine</h1>
        <form className="search-input" onSubmit={handleSearch}>
            <input 
                type="search" 
                placeholder="Type search query"
                value={search}
                onChange= {e => setSearch(e.target.value)}/>
        </form>
      </div>
    </header>
    <div className="search-results">
        {(results).map((result, i) => {
            return (
                <div className="single-result">
                    <h3 className="result-title">{result._source.title}</h3>
                    <p>
                        {result._source.text}
                    </p>
                    <button className="save-button" onClick={() => saveItem(result)}> 
                        Save to bookmarks
                    </button>
                </div>
            )
        })}
      </div>
    </div>
  );
}

export default Search;