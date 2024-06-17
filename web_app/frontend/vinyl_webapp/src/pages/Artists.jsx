import { useEffect, useState } from "react";
import TempPhoto from "../styles/images/image.png";
import { Img } from "react-image";
import axios from "axios";
import { Link } from "react-router-dom";

export default function Artists() {
  const [allArtists, setAllArtists] = useState([]);

  const getArtists = () => {
    axios.get("http://127.0.0.1:8000/vinyl_info/artists").then((response) => {
      console.log(response.data);
      setAllArtists(response.data);
    });
  };

  useEffect(() => {
    getArtists();
  }, []);

  return (
    <>
      {allArtists.length != 0 ? (
        <div className="catalog">
          <div className="catalog_title">
            <h1 className="title">Catalog</h1>
          </div>
          <div className="products">
            <div className="catalog_content">
              {allArtists.map((artist) => (
                <Link to={`/artists/${artist.slug}`} key={Math.random()}>
                  <div className="card">
                    <div className="temp">
                      <Img
                        src={
                          // eslint-disable-next-line no-prototype-builtins
                          artist.hasOwnProperty("imgur_img")
                            ? artist.imgur_img
                            : TempPhoto
                        }
                        className="card_img"
                      />
                    </div>
                    <div className="titles">
                      <p className="name">{artist.name}</p>
                    </div>
                  </div>
                </Link>
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
