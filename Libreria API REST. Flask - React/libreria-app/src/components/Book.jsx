import React from "react";
import { useHide } from "../hooks/useHide";

export const Book = ({ image, title, author, description }) => {
  const { hide, handleHide } = useHide();

  return (
    <article className="book_container">
      <img onClick={() => handleHide()} src={image} alt={title}></img>

      {hide ? (
        <div className="book_container_information">
          <h2>{title}</h2>
          <h3>{author}</h3>
          <p>{description}</p>
        </div>
      ) : (
        <></>
      )}
    </article>
  );
};
