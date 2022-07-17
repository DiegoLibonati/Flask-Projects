import React from "react";
import { useHide } from "../hooks/useHide";
import { FilterItem } from "./FilterItem";

export const FilterMenu = ({ genero, setBooks, filterName }) => {
  const { hide, handleHide } = useHide();

  return (
    <li onClick={handleHide}>
      {filterName}
      {hide ? (
        <ul>
          {genero.map((genero, index) => (
            <FilterItem
              key={index * 5231234120}
              setBooks={setBooks}
              genero={genero}
            ></FilterItem>
          ))}
        </ul>
      ) : (
        <></>
      )}
    </li>
  );
};
