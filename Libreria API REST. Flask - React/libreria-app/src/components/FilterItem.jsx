import React from "react";
import { useGetBooksByGenero } from "../hooks/useGetBooksByGenero";

export const FilterItem = ({ genero, setBooks }) => {
  const { books } = useGetBooksByGenero(genero);

  const handleFilter = () => {
    setBooks(books);
  };

  return <li onClick={() => handleFilter()}>{genero}</li>;
};
