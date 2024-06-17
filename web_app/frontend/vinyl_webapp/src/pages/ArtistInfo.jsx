import { useState, useEffect } from "react";
import TempPhoto from "../styles/images/image.png";
import { Img } from "react-image";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

export default function ArtistInfo() {
  const { slug } = useParams();
  const [artist, setArtist] = useState(null);
  const [vinylsOfArtist, setVinylsOfArtist] = useState([]);

  const getVinyl = () => {
    axios
      .get(`http://127.0.0.1:8000/vinyl_info/artists/${slug}`)
      .then((response) => {
        setArtist(response.data);
      });
  };

  const getArtistsVinyls = () => {
    axios
      .get(`http://127.0.0.1:8000/vinyl_info/artists/${slug}/all_vinyls`)
      .then((response) => {
        setVinylsOfArtist(response.data);
      });
  };

  useEffect(() => {
    getVinyl();
    getArtistsVinyls();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  return (
    <>
      {artist !== null && vinylsOfArtist.length != 0 ? (
        <>
          <div className="main_info">
            <div className="body_main">
              <div className="info">
                <h1 className="title_album">{artist.name}</h1>
                <p>{artist.profile}</p>
              </div>
              <div className="side_pic">
                <div className="album-cover">
                  <Img
                    src={artist.imgur_img ? artist.imgur_img : TempPhoto}
                    className="album_img"
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="other_content">
            <div className="discography">
              {vinylsOfArtist.map((vinyl, i) => (
                <div className="card" key={Math.random() * i}>
                  <Link to={`/vinyl/${vinyl.slug}`} className="card_link">
                    <Img
                      src={
                        // eslint-disable-next-line no-prototype-builtins
                        vinyl.hasOwnProperty("imgur_img")
                          ? vinyl.imgur_img
                          : TempPhoto
                      }
                      className="card_img"
                    />
                    <div className="titles">
                      <p className="name">{vinyl.name}</p>
                      {/* <a href="#" className="artist_link">
                        <p className="artists">Kendrick Lamar</p>
                      </a> */}
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <></>
      )}
    </>
  );
}
