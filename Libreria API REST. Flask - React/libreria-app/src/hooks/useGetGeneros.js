import { useEffect } from "react";
import { useState } from "react";

export const useGetGeneros = () => {
  const [genero, setGenero] = useState([]);

  const getGeneros = async () => {
    const request = await fetch("http://127.0.0.1:5000/libreria/generos");
    const response = await request.json();

    setGenero(response);
  };

  useEffect(() => {
    getGeneros();
  }, []);

  return {
    genero,
    setGenero,
  };
};
