import React from "react";
import { useHide } from "../hooks/useHide";
import { useState } from "react";
import { BsPlusCircle } from "react-icons/bs";

export const AddBook = ({ books, setBooks, genero, setGenero }) => {
  const { hide, handleHide } = useHide();

  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [gender, setGender] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState("");

  const handleChangeInputAuthor = (e) => {
    setAuthor(e.target.value);
  };

  const handleChangeInputTitle = (e) => {
    setTitle(e.target.value);
  };

  const handleChangeInputGender = (e) => {
    setGender(e.target.value);
  };

  const handleChangeInputDescription = (e) => {
    setDescription(e.target.value);
  };

  const handleChangeInputImage = (e) => {
    setImage(e.target.value);
  };

  const handleSubmit = async () => {
    const body = {
      title: title,
      author: author,
      description: description,
      image: image,
      genero: gender,
    };

    const result = await fetch("http://127.0.0.1:5000/libreria/crear", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (result.ok) {
      setBooks([...books, body]);

      if (!genero.includes(body.genero)) {
        setGenero([...genero, body.genero]);
      }
    }
  };

  return (
    <article className="book_container">
      <BsPlusCircle id="IconPlus" onClick={() => handleHide()}></BsPlusCircle>

      {hide ? (
        <form
          className="book_container_information"
          onSubmit={() => handleSubmit()}
        >
          <input
            type="text"
            placeholder="Set title"
            value={title}
            onChange={(e) => handleChangeInputTitle(e)}
          ></input>
          <input
            type="text"
            placeholder="Set author"
            value={author}
            onChange={(e) => handleChangeInputAuthor(e)}
          ></input>
          <input
            type="text"
            placeholder="Set gender"
            value={gender}
            onChange={(e) => handleChangeInputGender(e)}
          ></input>
          <textarea
            type="text"
            placeholder="Set description"
            value={description}
            onChange={(e) => handleChangeInputDescription(e)}
          ></textarea>
          <input
            type="text"
            placeholder="Set image link"
            value={image}
            onChange={(e) => handleChangeInputImage(e)}
          ></input>
          <button type="submit">Submit</button>
        </form>
      ) : (
        <></>
      )}
    </article>
  );
};
