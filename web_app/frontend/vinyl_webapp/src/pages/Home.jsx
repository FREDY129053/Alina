/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";
import TempPhoto from "../styles/images/image.png";
import { Img } from "react-image";
import axios from "axios";
import { Spin } from "antd";
import { Link } from "react-router-dom";

export default function Home() {
  const [filters, setFilters] = useState([]);
  const [allVinyls, setAllVinyls] = useState([]);
  const [country, setCountry] = useState("");
  const [sort, setSort] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [isSelected, setIsSelected] = useState(false);

  // const [currPage, setCurrPage] = useState(1);
  // const [isFetching, setIsFetching] = useState(true);

  const getDbFilters = () => {
    axios.get("http://127.0.0.1:8000/vinyl_info/filters").then((response) => {
      setFilters(response.data);
    });
  };

  const getVinyls = () => {
    let query = `http://127.0.0.1:8000/vinyl_info?`;

    if (sort !== "" && sort !== undefined) {
      query += `sort=${sort}&`;
    }

    if (country !== "" && country !== undefined) {
      query += `countries=${country}&`;
    }

    if (selectedGenres.length !== 0) {
      selectedGenres.forEach((genre) => {
        query += `genres=${genre}&`;
      });
    }

    axios.get(query).then((response) => {
      setAllVinyls(response.data.vinyls);
    });
    // .finally(() => setIsFetching(false));
  };

  useEffect(() => {
    getVinyls();
    getDbFilters();
  }, [country, sort, selectedGenres]);

  const handleCheckboxChange = (genre) => {
    setSelectedGenres((prevSelectedGenres) => {
      const updatedGenres = prevSelectedGenres.includes(genre)
        ? prevSelectedGenres.filter((g) => g !== genre)
        : [...prevSelectedGenres, genre];
      return updatedGenres;
    });
    setIsSelected(!isSelected);
  };

  return (
    <>
      {filters.length != 0 ? (
        <div className="catalog">
          <div className="catalog_title">
            <h1 className="title">Catalog</h1>
            <div className="sort_elements">
              <span>Sort by</span>
              <Dropdown
                text="Default"
                filters={["Name A-Z", "Name Z-A", "Rating Up", "Rating Down"]}
                value={sort}
                onChange={(o) => {
                  setSort(o);
                }}
                class_type={"sort"}
              />
            </div>
          </div>
          <div className="products">
            <div className="catalog_left-block">
              <div className="left-filters">
                <div className="genres">
                  <h2>Genre</h2>
                  {filters.genres.map((item) => (
                    <label className="ui-checkbox" key={Math.random() * 10}>
                      <span>{item}</span>
                      <input
                        type="checkbox"
                        className="ui-checkbox_gr"
                        onChange={() => handleCheckboxChange(item)}
                        checked={selectedGenres.includes(item)}
                      />
                    </label>
                  ))}
                </div>
                <div className="country">
                  <h2>Country</h2>
                  <Dropdown
                    text="All"
                    filters={filters.countries}
                    value={country}
                    onChange={(o) => {
                      setCountry(o);
                    }}
                    class_type={"filter"}
                  />
                </div>
                <div className="year"></div>
              </div>
            </div>
            {allVinyls.length != 0 ? (
              <div className="catalog_content">
                {allVinyls.map((vinyl) => (
                  <Link to={`/vinyl/${vinyl.slug}`} key={Math.random()}>
                    <div className="card">
                      <div className="temp">
                        <Img
                          src={
                            // eslint-disable-next-line no-prototype-builtins
                            vinyl.hasOwnProperty("imgur_img")
                              ? vinyl.imgur_img
                              : TempPhoto
                          }
                          className="card_img"
                        />
                      </div>
                      <div className="titles">
                        <p className="name">{vinyl.name}</p>
                        <p>
                          {Object.keys(vinyl.artists).map((item, i) => (
                            <React.Fragment key={i}>
                              <Link
                                to={`/artists/${vinyl.artists[item]["slug"]}`}
                              >
                                {vinyl.artists[item]["name"]}
                              </Link>
                              {i !== vinyl.artists.length - 1 && (
                                <span className="separator">, </span>
                              )}
                            </React.Fragment>
                          ))}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="empty_result_p">Nothing...</p>
            )}
          </div>
        </div>
      ) : (
        <>
          <Spin size="large" />
        </>
      )}
    </>
  );
}

export function Dropdown({ class_type, value, onChange, filters, text }) {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  function clearOptions() {
    onChange(undefined);
  }

  function selectOption(option) {
    if (option !== value) onChange(option);
  }

  function isOptionSelected(option) {
    return option === value;
  }

  useEffect(() => {
    if (isOpen) setHighlightedIndex(0);
  }, [isOpen]);

  return (
    <div
      onBlur={() => setIsOpen(false)}
      onClick={() => setIsOpen(!isOpen)}
      tabIndex={0}
      className={`${class_type === "sort" ? "sort" : "container"}`}
    >
      {
        <span className="value">
          {value === undefined || value === "" ? <label>{text}</label> : value}
        </span>
      }
      <button
        onClick={(e) => {
          e.stopPropagation();
          clearOptions();
        }}
        className="clear_btn"
      >
        &times;
      </button>
      <div className="divider"></div>
      <div className="caret"></div>
      <ul className={`options ${isOpen ? "show" : ""}`}>
        {filters.map((option, i) => (
          <li
            onClick={(e) => {
              e.stopPropagation();
              selectOption(option);
              setIsOpen(false);
            }}
            onMouseEnter={() => setHighlightedIndex(i)}
            key={i}
            className={`option ${isOptionSelected(option) ? "selected" : ""} ${
              i === highlightedIndex ? "highlighted" : ""
            }`}
          >
            {option}
          </li>
        ))}
      </ul>
    </div>
  );
}
