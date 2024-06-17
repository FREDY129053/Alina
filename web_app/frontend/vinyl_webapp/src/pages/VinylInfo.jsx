/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from "react";
import TempPhoto from "../styles/images/image.png";
import { Img } from "react-image";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
// import { Spin, Carousel } from "antd";
import { Spin } from "antd";
import Carousel from "react-bootstrap/Carousel";

export default function VinylInfo() {
  const { slug } = useParams();
  const [vinyl, setVinyl] = useState(null);

  const getVinyl = () => {
    axios.get(`http://127.0.0.1:8000/vinyl_info/${slug}`).then((response) => {
      setVinyl(response.data);
    });
  };

  useEffect(() => {
    getVinyl();
  }, [slug]);

  return (
    <>
      {vinyl ? (
        <div className="main_info">
          <div className="body_main">
            <h1 className="title_album">
              <span className="title_link">
                {Object.keys(vinyl.artists).map((item, i) => (
                  <React.Fragment key={i}>
                    <Link
                      to={`/artists/${vinyl.artists[item]["slug"]}`}
                      className="artist_link"
                    >
                      {vinyl.artists[item]["name"]}
                    </Link>
                    {i !== vinyl.artists.length - 1 && (
                      <span className="separator">, </span>
                    )}
                  </React.Fragment>
                ))}
              </span>
              <span> &#8212; {vinyl.name}</span>
            </h1>
            <div className="side_pic">
              <div className="album-cover">
                <Img
                  src={vinyl.imgur_img ? vinyl.imgur_img : TempPhoto}
                  className="album_img"
                />
              </div>
            </div>
            <div className="table_info">
              <table className="table">
                <tbody>
                  <tr>
                    <th scope="row">Country:</th>
                    <td>
                      {Object.keys(vinyl.country).map((item, i) => (
                        <React.Fragment key={i}>
                          {vinyl.country[i]}
                          {i !== vinyl.country.length - 1 && (
                            <span className="separator">, </span>
                          )}
                        </React.Fragment>
                      ))}
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">Released:</th>
                    <td>{vinyl.year}</td>
                  </tr>
                  <tr>
                    <th scope="row">Genre:</th>
                    <td>
                      {Object.keys(vinyl.genres).map((item, i) => (
                        <React.Fragment key={i}>
                          {vinyl.genres[i]}
                          {i !== vinyl.genres.length - 1 && (
                            <span className="separator">, </span>
                          )}
                        </React.Fragment>
                      ))}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div className="tracklist_main">
            <section className="tracklist">
              <header>
                <h2>Tracklist</h2>
              </header>
              <div className="content">
                <table className="table_tracklist">
                  <tbody>
                    {vinyl.tracklist.map((track, i) =>
                      i <= parseInt((60 / 100) * vinyl.tracklist.length) ? (
                        <tr key={Math.random() * 0.1}>
                          <td className="pos">A1</td>
                          <td className="space"></td>
                          <td className="track">{track.name}</td>
                          <td>{track.duration ? track.duration : ""}</td>
                        </tr>
                      ) : (
                        <tr key={Math.random()}>
                          <td className="pos">B1</td>
                          <td className="space"></td>
                          <td className="track">{track.name}</td>
                          <td>{track.duration ? track.duration : ""}</td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </div>
          {vinyl.imgur_all_photos ? (
            <Carousel className="carousel" controls={false}>
              {vinyl.imgur_all_photos.map((photo, i) => (
                <Carousel.Item interval={1500} key={Math.random() * i}>
                  <Img
                    src={photo.link}
                    width={500}
                    loader={<Spin className="" size="large" />}
                  />
                </Carousel.Item>
              ))}
            </Carousel>
          ) : (
            ""
          )}
        </div>
      ) : (
        <>Loh</>
      )}
    </>
  );
}

{
  /* <Carousel
              autoplay={true}
              infinite={true}
              className="carousel"
              autoplaySpeed={2000}
              // dotPosition="left"
              dotHeight={3}
            >
              {vinyl.imgur_all_photos.map((photo, i) => {
                return (
                  <div key={i}>
                    {console.log(photo.link)}
                    <Img
                      src={photo.link}
                      width={500}
                      loader={<Spin className="" size="large" />}
                    />
                  </div>
                );
              })}
            </Carousel> */
}
