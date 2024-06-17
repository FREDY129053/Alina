import "../src/styles/App.css";
import { Route, Routes, Link } from "react-router-dom";
import Home from "../src/pages/Home";
import ArtistInfo from "../src/pages/ArtistInfo";
import Artists from "../src/pages/Artists";
import VinylInfo from "../src/pages/VinylInfo";
import { useEffect, useState } from "react";

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
  // const [answerItems, setAnswerItems] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (search) {
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }

    // const TimeSleep = setTimeout(() => {
    // 	if (search) {
    // 		getInfoByName(search)
    // 	} else {
    // 		setSearchAnswer([])
    // 	}
    // }, 300);

    // return () => clearTimeout(TimeSleep)
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
      <div className="rightNav">
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
          <li>
            <img src="Gex68Hk.jpg" alt="" />
            Guardians Of The Galaxy (Songs From The Motion Picture)
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default App;
