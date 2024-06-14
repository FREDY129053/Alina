/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";
import TempPhoto from "../styles/images/Gex68Hk.jpg";
import { Img } from "react-image";
import axios from "axios";
import { Link } from "react-router-dom";

export default function Home() {
  const [filters, setFilters] = useState([]);
  const [allVinyls, setAllVinyls] = useState([]);
  const [countries, setCountries] = useState([]);

  const getDbFilters = () => {
    axios.get("http://127.0.0.1:8000/vinyl_info/filters").then((response) => {
      setFilters(response.data);
    });
  };

  const getVinyls = () => {
    axios.get("http://127.0.0.1:8000/vinyl_info/").then((response) => {
      setAllVinyls(response.data);
      console.log(response.data);
    });
  };

  useEffect(() => {
    getVinyls();
    getDbFilters();
  }, []);

  return (
    <>
      {allVinyls.length != 0 && filters.length != 0 ? (
        <div className="catalog">
          <div className="catalog_title">
            <h1 className="title">Catalog</h1>
            <div className="sort">
              <span>Sort by</span>
              <select name="sort" id="sort_top">
                <option value=""></option>
                <option value="">по названию А-Я</option>
                <option value="">по названию Я-А</option>
                <option value="">по убыванию рейтнга</option>
                <option value="">по возрастанию рейтинга</option>
              </select>
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
                      <input type="checkbox" className="ui-checkbox_gr" />
                    </label>
                  ))}
                </div>
                <div className="country">
                  <h2>Country</h2>
                  <Dropdown
                    text="All"
                    filters={filters.countries}
                    value={countries}
                    onChange={(o) => setCountries(o)}
                    multiple={false}
                  />
                </div>
                <div className="year"></div>
              </div>
            </div>
            <div className="catalog_content">
              {allVinyls.vinyls.map((vinyl) => (
                <div className="card" key={Math.random()}>
                  <Img src={TempPhoto} className="card_img" />
                  <div className="titles">
                    <p className="name">{vinyl.name}</p>
                    <p>
                      {Object.keys(vinyl.artists).map((item, i) => (
                        <React.Fragment key={i}>
                          <Link to={"/"}>{vinyl.artists[item]["name"]}</Link>
                          {i !== vinyl.artists.length - 1 && (
                            <span className="separator">, </span>
                          )}
                        </React.Fragment>
                      ))}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
}

export function Dropdown({ multiple, value, onChange, filters, text }) {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  function clearOptions() {
    multiple ? onChange([]) : onChange(undefined);
  }

  function selectOption(option) {
    if (multiple) {
      if (value.includes(option)) {
        onChange(value.filter((o) => o !== option));
      } else {
        onChange([...value, option]);
      }
    } else {
      if (option !== value) onChange(option);
    }
  }

  function isOptionSelected(option) {
    return multiple ? value.includes(option) : option === value;
  }

  useEffect(() => {
    if (isOpen) setHighlightedIndex(0);
  }, [isOpen]);

  return (
    <div
      onBlur={() => setIsOpen(false)}
      onClick={() => setIsOpen(!isOpen)}
      tabIndex={0}
      className="container"
    >
      {multiple ? (
        <span className="value">
          {value.length === 0 ? (
            <label>{text}</label>
          ) : (
            value.map((v, i) => (
              <button
                key={i}
                onClick={(e) => {
                  e.stopPropagation();
                  selectOption(v);
                }}
                className="option_badge"
              >
                {v}
                <span className="remove_btn">&times;</span>
              </button>
            ))
          )}
        </span>
      ) : (
        <span className="value">
          {console.log(value)}
          {value === undefined ? <label>{text}</label> : value}
        </span>
      )}
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
