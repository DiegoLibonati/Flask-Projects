import React from "react";
import "../css/config.css";
import "../css/books_container.css";
import { useGetBooks } from "../hooks/useGetBooks";
import { Book } from "./Book";
import { FilterItem } from "./FilterItem";
import { useHide } from "../hooks/useHide";
import { AddBook } from "./AddBook";
import { useGetGeneros } from "../hooks/useGetGeneros";

export const Main = () => {
  const { loading, books, defaultFetch, setBooks } = useGetBooks();
  const { hide, handleHide } = useHide();
  const { genero, setGenero } = useGetGeneros();

  if (loading) {
    return <h2>Loading</h2>;
  } else {
    return (
      <>
        <main className="main_container">
          <section className="config_container">
            <article className="filter_genero_container">
              <button onClick={() => handleHide()}>Filters</button>

              {hide ? (
                <ul className="filter_genero_container_list">
                  <li onClick={() => setBooks(defaultFetch)}>All</li>
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
            </article>
          </section>

          <section className="books_container">
            {books.map((book) => (
              <Book key={book._id.$oid} {...book}></Book>
            ))}

            <AddBook
              setBooks={setBooks}
              books={books}
              genero={genero}
              setGenero={setGenero}
            ></AddBook>
          </section>
        </main>
      </>
    );
  }
};
