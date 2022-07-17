import { useEffect } from "react";
import { useState } from "react";

export const useGetBooks = () => {
  const [defaultFetch, setDefaultFetch] = useState([]);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const getBooks = async () => {
    const request = await fetch("http://127.0.0.1:5000/libreria");
    const response = await request.json();

    setDefaultFetch(response);
    setBooks(response);
    setLoading(false);
  };

  useEffect(() => {
    getBooks();
  }, []);

  return {
    books,
    defaultFetch,
    loading,
    setBooks,
  };
};
