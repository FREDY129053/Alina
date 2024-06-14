import "../src/styles/App.css";
import { Route, Routes } from "react-router-dom";
import Home from "../src/pages/Home";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

function Navbar() {
  return (
    <nav className="navbar">
      <ul className="nav-list">
        <li>
          <a href="">Logo</a>
        </li>
        <li>
          <a href="">Vinyls</a>
        </li>
        <li>
          <a href="">Artists</a>
        </li>
      </ul>
      <div className="rightNav">
        <input
          type="text"
          name="search"
          id="search"
          placeholder="Search"
          autoComplete="off"
        />
        <button className="btn btn-sm">Search</button>
      </div>
    </nav>
  );
}

export default App;
