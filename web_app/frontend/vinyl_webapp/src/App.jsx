import "../src/styles/App.css";
import { Route, Routes, Link } from "react-router-dom";
import Home from "../src/pages/Home";
import ArtistInfo from "../src/pages/ArtistInfo";
import Artists from "../src/pages/Artists";
import VinylInfo from "../src/pages/VinylInfo";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Img } from "react-image";
import TempPhoto from "../src/styles/images/image.png";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/artists" element={<Artists />} />
        <Route path="/artists/:slug" element={<ArtistInfo />} />
        <Route path="/vinyl/:slug" element={<VinylInfo />} />
      </Routes>
    </>
  );
}

function Navbar() {
  const [search, setSearch] = useState("");
  const [answerItems, setAnswerItems] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const divRef = useRef(null);

  const searchResults = (search_input) => {
    axios
      .get(`http://127.0.0.1:8000/vinyl_info/search/${search_input}`)
      .then((response) => {
        setAnswerItems(response.data);
      });
  };

  const handleClickOutside = (e) => {
    if (divRef.current && !divRef.current.contains(e.target)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    const handleBodyClick = (e) => {
      handleClickOutside(e);
      setSearch("");
    };

    document.body.addEventListener("click", handleBodyClick);

    return () => {
      document.body.removeEventListener("click", handleBodyClick);
    };
  }, []);

  useEffect(() => {
    if (search) {
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }

    const TimeSleep = setTimeout(() => {
      if (search) {
        searchResults(search);
      } else {
        setAnswerItems([]);
      }
    }, 300);

    return () => clearTimeout(TimeSleep);
  }, [search]);

  return (
    <nav className="navbar">
      <ul className="nav-list">
        <li>
          <Link to={"/"}>Logo</Link>
        </li>
        <li>
          <Link to={"/"}>Vinyls</Link>
        </li>
        <li>
          <Link to={"/artists"}>Artists</Link>
        </li>
      </ul>
      <div className="rightNav" onBlur={handleClickOutside} ref={divRef}>
        <input
          type="text"
          name="search"
          id="search"
          placeholder="Search"
          autoComplete="off"
          onChange={(e) => setSearch(e.target.value)}
          value={search}
        />
        <ul className={`search_options ${isOpen ? "show" : ""}`}>
          {answerItems.map((item, i) => (
            <Link
              className="search_link"
              to={`/vinyl/${item.slug}`}
              key={Math.random() * i - 1}
              onClick={() =>
                setTimeout(() => {
                  setIsOpen(false);
                  setSearch("");
                }, 50)
              }
            >
              <li>
                <Img src={item.imgur_img ? item.imgur_img : TempPhoto} />
                {item.name}
              </li>
            </Link>
          ))}
        </ul>
      </div>
    </nav>
  );
}

export default App;
