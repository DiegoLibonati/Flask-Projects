import { useEffect } from "react";
import { useState } from "react";

export const useGetBooksByGenero = (genero) => {
  const [books, setBooks] = useState([]);

  const getBooksByGenero = async () => {
    const request = await fetch(`http://127.0.0.1:5000/libreria/${genero}`);
    const response = await request.json();
    setBooks(response);
  };

  useEffect(() => {
    getBooksByGenero();
  }, []);

  return {
    books,
  };
};
